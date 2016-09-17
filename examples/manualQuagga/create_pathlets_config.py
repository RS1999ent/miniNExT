import QuaggaTopo_pb2
import quagga_config_pb2

def CreatePathletsConfig(protobuf_hosts):
    # Creates quagga_config proto protobuf config in the configuration
    # directories of hosts.
    #
    # Arguments:
    #   protobuf_hosts: the list of hosts to generate configs for. In
    #   QuaggaTopoForm
    #
    # Returns: a dictionary of a hsot to a quaga_cofnig pathlet prot oobject.

    return_dict = {}
    for host in protobuf_hosts:
        hostname = host.host_name
        is_border_router = 0
        if host.is_border_router == '':
            is_border_router = 0
        else:
            is_border_router = host.is_border_router
        pathlet_config = quagga_config_pb2.PathletProtoConfig()
        pathlet_config.is_island_border_router = is_border_router
        pathlet_config.private_slash24_ip = host.private_pathlet_ip
        return_dict[hostname] = pathlet_config
    return return_dict




