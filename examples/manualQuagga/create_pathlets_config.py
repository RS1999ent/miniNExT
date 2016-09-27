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
        if host.HasField("manual_two_hop"):
            mn_filter = host.manual_two_hop;
            quagga_config_filter = quagga_config_pb2.Filter()
            quagga_config_filter.one_hop_ip = mn_filter.one_hop_ip
            manual_pathlet = quagga_config_pb2.ManualPathlet()
            manual_pathlet.vnode1 = mn_filter.pathlet_to_advertise.vnode1
            manual_pathlet.vnode2 = mn_filter.pathlet_to_advertise.vnode2
            manual_pathlet.destination = mn_filter.pathlet_to_advertise.destination
            quagga_config_filter.pathlet_to_advertise.CopyFrom(manual_pathlet)
            pathlet_config.filters.add().CopyFrom(quagga_config_filter)
        return_dict[hostname] = pathlet_config
    return return_dict




