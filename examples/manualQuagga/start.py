#!/usr/bin/python

"""
Example network of Quagga routers
(QuaggaTopo + QuaggaService)
"""

import sys
import atexit

# patch isShellBuiltin
import mininet.util
import mininext.util
mininet.util.isShellBuiltin = mininext.util.isShellBuiltin
sys.modules['mininet.util'] = mininet.util

from mininet.util import dumpNodeConnections
from mininet.node import OVSController
from mininet.log import setLogLevel, info

from mininext.cli import CLI
from mininext.net import MiniNExT

from topo import QuaggaTopo
import QuaggaTopo_pb2
from protobuf_config_parser import ProtobufConfigParser
from generate_quagga_configs import GenerateQuaggaConfigs
import jinja2
import create_configs_and_directory_structure
import argparse

net = None

def InitializeArgParser():
    """  asdfasdf"""
    return 1

def startNetwork(host_protos):
    """instantiates a topo, then starts the network and prints debug information
    arguments:
    host_protos: used by QuaggaTopo to instantiate the correct hosts
    """


    info('** Creating Quagga network topology\n')
    topo = QuaggaTopo(host_protos)
    # topo.CreateMininetQuaggaTopo(host_protos)

    info('** Starting the network\n')
    global net
    net = MiniNExT(topo, controller=OVSController)
     
    #    net.staticArp()
    net.start()

    info('** Dumping host connections\n')
    dumpNodeConnections(net.hosts)

    #   info('** Testing network connectivity\n')
    #   net.ping(net.hosts)

    info('** Dumping host processes\n')
    for host in net.hosts:
        host.cmdPrint("ps aux")

    info('** Running CLI\n')
    # net.startTerms()
    CLI(net)


def stopNetwork():
    "stops a network (only called on a forced cleanup)"

    if net is not None:
        info('** Tearing down Quagga network\n')
        net.stop()

if __name__ == '__main__':
    # Force cleanup on exit by registering a cleanup function
    atexit.register(stopNetwork)

    # Tell mininet to print useful information
    setLogLevel('info')


    # handle config specification
    config_parser = ProtobufConfigParser()
    protobuf_config_file_handle = open('protobufconfig', 'r')
    config_parser.parseProtobufConfig(protobuf_config_file_handle)
    host_protos = config_parser.protobuf_Hosts_
    topology_protos = config_parser.protobuf_Topologys_

    # handle generating quagga bgpd config dictionary
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="."),
                                   trim_blocks=True,
                                   lstrip_blocks=True)
    generate_quagga_configs = GenerateQuaggaConfigs(host_protos, topology_protos, jinja_env)
    hostname_to_bgpdconfig = generate_quagga_configs.CreateBgpdConfigs()

    # Write configs to file system
    # create_configs_and_directory_structure.WriteConfigs(hostname_to_bgpdconfig)

    #start up mininet
    startNetwork(host_protos)
