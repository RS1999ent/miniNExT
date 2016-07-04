"""
Example topology of Quagga routers
"""

import inspect
import os
import QuaggaTopo_pb2
from mininext.topo import Topo
from mininext.services.quagga import QuaggaService

from collections import namedtuple

QuaggaHost = namedtuple("QuaggaHost", "name ip loIP")
net = None


class QuaggaTopo(Topo):

    "Creates a topology of Quagga routers"

    def __init__(self, host_protos):
        """ Initialize a Quagga topology with 5 routers, configure their IP
           addresses, loop back interfaces, and paths to their private
           configuration directories. """
        Topo.__init__(self)
        # Directory where this file / script is located"
        selfPath = os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe())))  # script directory

        # Initialize a service helper for Quagga with default options
        quaggaSvc = QuaggaService(autoStop=False)

        # Path configurations for mounts
        quaggaBaseConfigPath = selfPath + '/configs/'

        ixpfabric = self.addSwitch('fabric-sw1')

        for host_proto in host_protos:
            print 'HOSTNAME', host_proto.host_name
            print 'hostip', host_proto.ip
            hostname = str(host_proto.host_name)
            hostip = str(host_proto.ip)
            quagga_container = self.addHost(name=hostname,
                                           ip=hostip,
                                           hostname=hostname,
                                           privateLogDir=True,
                                           privateRunDir=True,
                                           inMountNamespace=True,
                                           inPIDNamespace=True,
                                           inUTSNamespace=True)
            print quagga_container
            # quagga_container = self.addHost(name = host_proto.host_name,
            #                                 ip=host_proto.ip + '/16',
            #                                 hostname=host_proto.host_name,
            #                                 privateLogDir=True,
            #                                 privateRunDir=True,
            #                                 inMountNamespace=True,
            #                                 inPIDNamespace=True,
            #                                 inUTSNamespace=True)
            if host_proto.HasField('lo_ip'):
                # Add a loopback interface with an IP in router's announced range
                loip = str(host_proto.lo_ip)
                self.addNodeLoopbackIntf(node=host_proto.host_name, ip=loip) 

            # Configure and setup the Quagga service for this node
            quaggaSvcConfig = \
                {'quaggaConfigPath': quaggaBaseConfigPath + hostname}
            print quaggaSvcConfig
            self.addNodeService(node=hostname, service=quaggaSvc,
                                nodeConfig=quaggaSvcConfig)

            # Attach the quaggaContainer to the IXP Fabric Switch
            self.addLink(quagga_container, ixpfabric)


    # def CreateMininetQuaggaTopo(self, host_protos):
    #     """Given a list of host protobuf messages, create a simple mininet
    #     topology with one switch and hosts connected to it

    #     Arguments:
    #        host_protos: list of host protobuf messages that have
    #        configuration information for the hosts. This function will only use
    #        mininet related information necessary to create topology, no quagga
    #        specific configs are generated or considerd.

    #     """

    #     # Directory where this file / script is located"
    #     selfPath = os.path.dirname(os.path.abspath(
    #         inspect.getfile(inspect.currentframe())))  # script directory

    #     # Initialize a service helper for Quagga with default options
    #     quaggaSvc = QuaggaService(autoStop=False)

    #     # Path configurations for mounts
    #     quaggaBaseConfigPath = selfPath + '/configs/'

    #     ixpfabric = self.addSwitch('fabric-sw1')

    #     for host_proto in host_protos:
    #         quagga_container = self.addHost(name=host_proto.host_name,
    #                                        ip=host_proto.ip,
    #                                        hostname=host_proto.host_name,
    #                                        privateLogDir=True,
    #                                        privateRunDir=True,
    #                                        inMountNamespace=True,
    #                                        inPIDNamespace=True,
    #                                        inUTSNamespace=True)
    #         print quagga_container
    #         # quagga_container = self.addHost(name = host_proto.host_name,
    #         #                                 ip=host_proto.ip + '/16',
    #         #                                 hostname=host_proto.host_name,
    #         #                                 privateLogDir=True,
    #         #                                 privateRunDir=True,
    #         #                                 inMountNamespace=True,
    #         #                                 inPIDNamespace=True,
    #         #                                 inUTSNamespace=True)
    #         if host_proto.HasField('lo_ip'):
    #             # Add a loopback interface with an IP in router's announced range
    #             self.addNodeLoopbackIntf(node=host_proto.host_name, ip=host_proto.lo_ip + '/16') 

    #         # Configure and setup the Quagga service for this node
    #         quaggaSvcConfig = \
    #             {'quaggaConfigPath': quaggaBaseConfigPath + host_proto.host_name}
    #         print quaggaSvcConfig
    #         self.addNodeService(node=host_proto.host_name, service=quaggaSvc,
    #                             nodeConfig=quaggaSvcConfig)

    #         # Attach the quaggaContainer to the IXP Fabric Switch
    #         self.addLink(quagga_container, ixpfabric)

