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
        wiser_protocol_config = quagga_config_pb2.WiserProtocolConfig()
        print 'IN CREATE WISER CONFIGS'

        #for each host in the protobuf hosts, make sure that it is not a
        #lookupservice node. Then for each entry in the topology where it is
        #the primary node, add Link with the remote addr and link cost. These
        #two things should make a nodelink.
        for host_proto in self.protobuf_hosts_:
            if host_proto.host_type != QuaggaTopo_pb2.HostType.Value('HT_QUAGGA'):
                continue
            node_link = quagga_config_pb2.NodeLink()
            hostname = host_proto.host_name
            local_addr = host_proto.ip
            node_link.primary_node.CopyFrom(self.CreateNodeProperty(hostname, local_addr))
            #not efficient, but just fund the adjacent nodes quikly
            adjacent_links = []
            if self.protobuf_topologys_ != None:
                for adjacency_list_entry in self.protobuf_topologys_[0].adjacency_list_entries:
                    if adjacency_list_entry.primary_node_name == hostname:
                        for adjacent_node_link in adjacency_list_entry.links:
                            adjacent_links.append(adjacent_node_link)
                        break
            #add a link for each adjacent link to node_link (this is what is
            #being added to the config)
            for link in adjacent_links:
                adjacenthost = self.FindHostProtoFromName(link.adjacent_node_name)
                adjacentnodename = link.adjacent_node_name
                adjacent_addr = adjacenthost.ip
                linkcost = link.link_cost
                proto_link = self.CreateLink(adjacentnodename, adjacent_addr, linkcost)
                #copy the created link into thisone
                node_link.links.add().CopyFrom(proto_link)
            if len(adjacent_links) >= 1:
                wiser_protocol_config.topology.node_links.add().CopyFrom(node_link)
        for hostproto in self.protobuf_hosts_:
            if hostproto.host_type != QuaggaTopo_pb2.HostType.Value('HT_QUAGGA'):
                continue
            hostname = hostproto.host_name
            #UGLY HACKS HERE TODO: make better
            general_config = quagga_config_pb2.Configuration()
            general_config.protocol_type = quagga_config_pb2.ProtocolType.Value('PT_WISER')
            general_config.wiser_protocol_config.CopyFrom(wiser_protocol_config)
            # return_dict[hostname] = wiser_protocol_config
            return_dict[hostname] = general_config
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
        return_link.adjacent_node.CopyFrom(self.CreateNodeProperty(hostname, interfaceip))
        return_link.link_cost = linkcost
        return return_link

    # Given a hostname, find the corresponding host proto in the class data
    # structure. This is not an efficient implementation
    #
    # Arguments:
    #   hostname: the name of the host to find.
    #
    # Returns: The corresponding proto that is the host. Empty if host does not
    # exist
    def FindHostProtoFromName(self, hostname):
        return_host = QuaggaTopo_pb2.Host()
        for host in self.protobuf_hosts_:
            if host.host_name == hostname:
                return host

