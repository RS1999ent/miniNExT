import QuaggaTopo_pb2
import quagga_config_pb2

class GenerateWiserConfigs():
    """Class responsible for generating a list of configs that are later to be
written to a file. These configs are specific to the wiser protocol information
that quagga wants. """

    protobuf_hosts_ = None
    protobuf_topologys_ = None

    def __init__(self, protobuf_hosts, protobuf_topologys):
        """Just initialize class variables"""
        self.protobuf_hosts_ = protobuf_hosts
        self.protobuf_topologys_ = protobuf_topologys

    def CreateWiserConfigs(self):
        """from the list of hosts and topology passed in on construction, create a
dictionary of hostname to the wiserprotocolconfig protobufs returns: A
dictionary keyed on the host name and the WiserProtocolConfig as the value """
        return_dict = {}

        #for each host in the protobuf hosts, make sure that it is not a
        #lookupservice node. Then for each entry in the topology where it is
        #the primary node, add Link with the remote addr and link cost. These
        #two things should make a nodelink.
        for host_proto in self.protobuf_hosts_:
            if host_proto.host_type == QuaggaTopo_pb2.HostType.Value('HT_LOOKUPSERVICE'):
                continue
            hostname = host_proto.host_name
            local_addr = host_proto.ip
        return return_dict

    # creates a quagga_config::NodeProperty from a hostname and interfaceip
    #
    # Arguments:
    #   hostname: the name to put in NodeProperty.node_name
    #   interfaceip: the ip to put in NOdeProperty.interface_ip
    #
    # Returns a nodeproperty with these fields filled in.
    def CreateNodeProperty(self, hostname, interfaceip):
        return_node_property = quagga_config_pb2.NodeProperty()
        return_node_property.node_name = hostname
        return_node_property.interface_ip = interfaceip
        return return_node_property

    # Creates a link from a hostname, interfaceip, and linkcost
    #
    # Arguments:
    #   hostname: the nodename in the nodeproperty of a link
    #   interfaceip: the interface_ip in the nodeproperty in the link
    #   lihnkcost : the cost of the link
    #
    # Returns: A quagga_config::Link with the adjacent node proptery filled in
    # with the link cost set
    def CreateLink(self, hostname, interfaceip, linkcost):
        return_link = quagga_config_pb2.Link()
        return_link.adjacent_node = CreateNodeProperty(hostname, interfaceip)
        return_link.link_cost = linkcost
        return returnlink
