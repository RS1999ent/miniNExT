import QuaggaTopo_pb2
import quagga_config_pb2
import create_pathlets_config
from  generate_wiser_configs import GenerateWiserConfigs



def GetIslandIdToIslandMembers(protobuf_hosts):
    # Goes through protobuf_hosts and returns a dictionary of the island_id to
    # a list of Ases that are a part of that island.
    #
    # Arguments:
    #   protobuf_hosts: The list of QuaggaTopo.proto type hosts that have island_ids.
    #
    # Returns: A dictionary of an island id to a list of asnums in that island.
    # {34 : [1, 2, 3]}

    return_dict = {}
    # for each host, add the as to the corresponding island id list. If it
    # doesn't exist, create one
    for host in protobuf_hosts:
        if host.island_id not in return_dict:
            return_dict[host.island_id] = []
        return_dict[host.island_id].append(host.as_num)
    return return_dict



def CreateGeneralConfigs(protobuf_hosts, protobuf_topology):
    # Creates quaga_config.proto general configs to be place in the config
    # directories of hosts.
    #
    # Arguments:
    #   protobuf_hosts: the list of hosts to generate configs for. These are
    #   protrobufs of QuaggaTopo form
    #   protobuf_topology: QuaggaTopo.proto of the router level topology
    #
    # Returns: a dictionary of a host to a quagga_config configuration proto
    # object.

    return_dict = {}

    #Get the island ids to island members for generating wiser configs
    island_ids_to_islandmembers = GetIslandIdToIslandMembers(protobuf_hosts)
    host_to_wiserconfigs = {}

    # Generate wiser configs
    # made protobuf_topology a list becuase that is what GenerateWiserConfigs
    # expects.
    topo_list = []
    topo_list.append(protobuf_topology)
    generate_wiser_configs = GenerateWiserConfigs(protobuf_hosts, topo_list)
    host_to_wiserconfigs = generate_wiser_configs.CreateWiserConfigs()
    # generate pathlet ocnfigs
    host_to_pathletconfigs = create_pathlets_config.CreatePathletsConfig(protobuf_hosts)

    # for each host, create a general config Configuration object from the
    # host_to_wiserconfigs and 'island_ids_to_islandmembers'.
    for host in protobuf_hosts:
        general_config = quagga_config_pb2.Configuration()
        hostname = host.host_name
        if hostname in host_to_wiserconfigs:
            general_config.wiser_protocol_config.CopyFrom(host_to_wiserconfigs[hostname])
        if hostname in host_to_pathletconfigs:
            general_config.pathlet_config.CopyFrom(host_to_pathletconfigs[hostname])
        # for each as that is a member of this island id, if the member does
        # not denote this host, then add it to the general_config
        # island_members
        island_id = host.island_id
        general_config.island_id = island_id
        for member_as in island_ids_to_islandmembers[island_id]:
            if member_as != host.as_num:
                general_config.island_member_ases.append(member_as)
        #make protocol wiser for now TODO 
        if host.protocol == 'wiser':
            general_config.protocol_type = quagga_config_pb2.ProtocolType.Value('PT_WISER')
        elif host.protocol == 'pathlets':
            general_config.protocol_type = quagga_config_pb2.ProtocolType.Value('PT_PATHLETS')
        elif host.protocol == 'baseline_sleeper':
            general_config.protocol_type = quagga_config_pb2.ProtocolType.Value('PT_BASELINE_SLEEPER')
        else:
            general_config.protocol_type = quagga_config_pb2.ProtocolType.Value('PT_BASELINE')


        return_dict[hostname] = general_config
        print general_config


    

    return return_dict
