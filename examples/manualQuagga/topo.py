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


class QuaggaTopo(Topo):

    "Creates a topology of Quagga routers"

    def __init__(self, host_protos):
        """ Initialize a Quagga topology with 5 routers, configure their IP
           addresses, loop back interfaces, and paths to their private
           configuration directories.
        """
        Topo.__init__(self)
        # Directory where this file / script is located"
        selfPath = os.path.dirname(
            os.path.abspath(inspect.getfile(inspect.currentframe(
            ))))  # script directory

        # Initialize a service helper for Quagga with default options
        quaggaSvc = QuaggaService(autoStop=False)

        # Path configurations for mounts
        quaggaBaseConfigPath = selfPath + '/configs/'

        ixpfabric = self.addSwitch('fabric-sw1')

        for host_proto in host_protos:
            # if(host_proto.host_type == QuaggaTopo_pb2.HostType.Value('HT_LOOKUPSERVICE')):
            #     self.InitializeLookUpServiceNode(ixpfabric, host_proto, quaggaBaseConfigPath)
            # if(host_proto.host_type == QuaggaTopo_pb2.HostType.Value('HT_QUAGGA')):
            self.InitializeQuaggaServiceNode(ixpfabric, host_proto, quaggaBaseConfigPath)

# private methods below here

    def InitializeLookUpServiceNode(self, ixp_fabric, host_proto, config_path):
        print 'HOSTNAME', host_proto.host_name
        print 'hostip', host_proto.ip
        hostname = str(host_proto.host_name)
        hostip = str(host_proto.ip)
        lookupservice_container = self.addHost(
            name=hostname,
            ip=hostip,
            hostname=hostname,
            privateLogDir=True,
            privateRunDir=True,
            inMountNamespace=True,
            inPIDNamespace=True,
            inUTSNamespace=True)
        print lookupservice_container
        if host_proto.HasField('lo_ip'):
            # Add a loopback interface with an IP in router's announced range
            loip = str(host_proto.lo_ip) + '/24'
            self.addNodeLoopbackIntf(node=host_proto.host_name, ip=loip)

        # Configure and setup the Quagga service for this node
        lookup_service_config = \
            {'quaggaConfigPath': config_path + hostname}
        print lookup_service_config
        # self.addNodeService(
        #     node=hostname, service=None, nodeConfig=lookup_service_config)

        # Attach the quaggaContainer to the IXP Fabric Switch
        self.addLink(lookupservice_container, ixp_fabric)

    def InitializeQuaggaServiceNode(self, ixp_fabric, host_proto, config_path):
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
        if host_proto.HasField('path_to_executable'):
            path_to_bgpd = str(host_proto.path_to_executable)
            print "Path to bgpd: ", path_to_bgpd
            self.addNodeService(
                node=hostname,
                service=ManualQuaggaService(
                    path_to_bgpd, autoStop=False),
                nodeConfig=quaggaSvcConfig)
        else:
            self.addNodeService(
                node=hostname, service=QuaggaService(autoStop=False), nodeConfig=quaggaSvcConfig)

        # Attach the quaggaContainer to the IXP Fabric Switch
        self.addLink(quagga_container, ixp_fabric)
