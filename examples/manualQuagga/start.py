#!/usr/bin/python

"""
Example network of Quagga routers
(QuaggaTopo + QuaggaService)
"""

import sys
import subprocess
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
from generate_wiser_configs import GenerateWiserConfigs
from generate_general_configs import CreateGeneralConfigs
import jinja2
import create_configs_and_directory_structure
import argparse

net = None
kMxLocation = 'utils/mx'

def InitializeArgParser():
    """ Function where you should add additional command line arguments.

    Returns: the return of argparse.parse_args()"""

    parser = argparse.ArgumentParser()
    #add argument for the configuration file
    parser.add_argument('-f', '--protobuf_config_file',
                        default='protobufconfig',
                        help='File where the general configuration for the program is stored as specified by QuaggaTopo.proto')
    return parser.parse_args()

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

    # start up redis on the lookup service host (specified in
    # host_protos)
    StartUpRedis(host_protos)
    CLI(net)

def StartUpRedis(host_protos):
    """ Given a list of host protos, run external program 'mx' that allows one to
    start up a program on an running host container. This function will use that
    program to start up redis on the appropraite hosts.

    Arguments:
       host_protos: list of host protobuf messages as defined in
       QuaggaTopo.proto, only the one with type HT_LOOKUPSERVICE will have
       redis started on it.
    
    """
    #find lookup service host proto host name
    lookupservice_host_name = ''
    redis_path = ''
    for host_proto in host_protos:
        if(host_proto.host_type == QuaggaTopo_pb2.HostType.Value('HT_LOOKUPSERVICE')):
            lookupservice_host_name = host_proto.host_name
            redis_path = host_proto.path_to_redis_executable
            break

    #run mx <host_name> <path_to_redis> commandline
    command = './' + kMxLocation + ' ' + lookupservice_host_name + ' ' + redis_path
    print command
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # print 'starting redis command'
    # print p.stdout.readlines()
    # print p.stderr


def stopNetwork():
    "stops a network (only called on a forced cleanup)"

    if net is not None:
        info('** Tearing down Quagga network\n')
        net.stop()
    # cleanup generated configs
    create_configs_and_directory_structure.DeleteConfigs()

if __name__ == '__main__':
    # clear logs
    command = "sudo ./utils/clear_mininext_host_logs.sh"
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    #parse commandline arguments
    args = InitializeArgParser()
    print args
    # Force cleanup on exit by registering a cleanup function
    atexit.register(stopNetwork)

    # Tell mininet to print useful information
    setLogLevel('info')


    # handle config specification
    config_parser = ProtobufConfigParser()
    protobuf_config_file_handle = open(args.protobuf_config_file, 'r')
    config_parser.parseProtobufConfig(protobuf_config_file_handle)
    host_protos = config_parser.protobuf_Hosts_
    topology_protos = config_parser.protobuf_Topologys_

    # handle generating quagga bgpd config dictionary
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="."),
                                   trim_blocks=True,
                                   lstrip_blocks=True)
    generate_quagga_configs = GenerateQuaggaConfigs(host_protos, topology_protos, jinja_env)
    hostname_to_bgpdconfig = generate_quagga_configs.CreateBgpdConfigs()

    #handle generating general config
    hostname_to_generalconfig = CreateGeneralConfigs(host_protos, topology_protos[0])
    print 'HOSTNAME TO GENERAL CONFIG', hostname_to_generalconfig

    # Write configs to file system
    create_configs_and_directory_structure.WriteConfigs(hostname_to_bgpdconfig, hostname_to_generalconfig)

    #start up mininet
    startNetwork(host_protos)
