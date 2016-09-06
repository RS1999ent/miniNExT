"""
Example topology of Quagga routers
"""

import inspect
import os
import QuaggaTopo_pb2
from mininext.topo import Topo
from mininext.services.quagga import QuaggaService
from mininext.services.manual_quagga_service import ManualQuaggaService

from collections import namedtuple

QuaggaHost = namedtuple("QuaggaHost", "name ip loIP")
net = None


def CreateTopologyAdjacencyList(topology):
    """Creates a hostname to adjecencylist topology. The adjecencyu list returned has
no redundant entries and therefore it is assumed that links are symmetric. No
redundancy means that if a link is specified in the adjacency list, the reverse
is not specified in the adjacency list.

        Arguments:
           topology: The 'Topology' protobuf to create an adjacency list from

        Returns: A hostname to adjacency list {hostname: []} dictionary
        """
    return_dict = {}
    #for each entry, add it an entry to the return dict. The adjacent nodes
    #should be only added if the adjacent node does not have a primary entry.
    #If it does have a primary entry, then the link was already added, so you
    #would be adding a redundant link.
    for adjacency_list_entry in topology.adjacency_list_entries:
        primary_node_name = adjacency_list_entry.primary_node_name
        adjacent_nodes = []
        for link in adjacency_list_entry.links:
            adjacent_node_name = link.adjacent_node_name
            if adjacent_node_name not in return_dict:
                adjacent_nodes.append(link.adjacent_node_name)
        # add to dict only if adjacent nodes are greater than 0, this means
        # that this has new information. If there are no adjacent nodes, then
        # this primary node is already covered in the dict. No Redudancy is the
        # key.
        if len(adjacent_nodes) > 0:
            return_dict[primary_node_name] = adjacent_nodes

    return return_dict


class QuaggaTopo(Topo):

    "Creates a topology of Quagga routers"

    # topology_ = None
    # host_protos_ = None
    quagga_base_config_path_ = None

    def __init__(self):
        """ Initialize a Quagga topology with 5 routers, configure their IP
           addresses, loop back interfaces, and paths to their private
           configuration directories.
        """
        Topo.__init__(self)
        # Directory where this file / script is located"
        selfPath = os.path.dirname(
            os.path.abspath(inspect.getfile(inspect.currentframe(
            ))))  # script directory

        # Path configurations for mounts
        self.quagga_base_config_path_ = selfPath + '/configs/'

    def CreateTopology(self, host_protos, topology):
        """Creates a mininext topology with the hosts defined in 'host_protos' connected
to each other in the way defined by 'topology'

        Arguments:
           host_protos: A list of 'Host' protobufs containing the information
           for creating mininext hosts.
           topology: A 'Topology' type protobuf defining how hosts are to be
           connected to each other.
        """

        # Dictionary that maps a hostname to a mininet container. Used for
        # connected hosts together based on the topology.
        hostname_to_mn_container = {}
        for host_proto in host_protos:
            mn_container = self.InitializeQuaggaServiceNode(
                host_proto, self.quagga_base_config_path_)
            hostname_to_mn_container[host_proto.host_name] = mn_container

        hostname_to_adjacencylist = CreateTopologyAdjacencyList(topology)
        #add the links
        for hostname, adjecencylist in hostname_to_adjacencylist.iteritems():
            host_mn_container = hostname_to_mn_container[hostname]
            for adjacenthost in adjecencylist:
                adjacent_container = hostname_to_mn_container[adjacenthost]
                self.addLink(host_mn_container, adjacent_container)
        # private methods below here

    def InitializeQuaggaServiceNode(self, host_proto, config_path):
        """Initializes a node with a quagga service and returns the container.

        Arguments:

           host_proto: the 'Host' protobuf containing the information necessary
           to create a quagga service node.
           config_path: The path where the quagga configurations are stored.

        Returns: A mininet host container.
        """

        print 'HOSTNAME', host_proto.host_name
        print 'hostip', host_proto.ip
        hostname = str(host_proto.host_name)
        hostip = str(host_proto.ip)
        quagga_container = self.addHost(
            name=hostname,
            ip=hostip,
            hostname=hostname,
            privateLogDir=True,
            privateRunDir=True,
            inMountNamespace=True,
            inPIDNamespace=True,
            inUTSNamespace=True)
        print quagga_container
        if host_proto.HasField('lo_ip'):
            # Add a loopback interface with an IP in router's announced range
            loip = str(host_proto.lo_ip) + '/24'
            print "loopbackip is: ", loip
            self.addNodeLoopbackIntf(node=host_proto.host_name, ip=loip)

        # Configure and setup the Quagga service for this node
        quaggaSvcConfig = \
            {'quaggaConfigPath': config_path + hostname}
        print quaggaSvcConfig
        if host_proto.HasField('path_to_initd'):
            path_to_initd = str(host_proto.path_to_initd)
            print "Path to initd: ", path_to_initd
            self.addNodeService(
                node=hostname,
                service=ManualQuaggaService(
                    path_to_initd, autoStop=False),
                nodeConfig=quaggaSvcConfig)
        else:
            self.addNodeService(
                node=hostname,
                service=QuaggaService(autoStop=False),
                nodeConfig=quaggaSvcConfig)

        return quagga_container
        # Attach the quaggaContainer to the IXP Fabric Switch
        # self.addLink(quagga_container, ixp_fabric)
