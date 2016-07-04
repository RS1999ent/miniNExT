import QuaggaTopo_pb2
import jinja2

class GenerateQuaggaConfigs():
    """Class responsible for generating a list of configs that are later be written
    to a file. Input to the class will be the Host list and topology protobuf
    message types.
    The jinja2_env should contain:
    quagga_bgpd_template.j2

    """

    protobuf_Hosts_ = None
    protobuf_Topologys_ = None
    jinja2_env_ = None

    def __init__(self, protobuf_Hosts, protobuf_Topologys, jinja2_env):
        """Just initializes class variables"""
        self.protobuf_Hosts_ = protobuf_Hosts
        self.protobuf_Topologys_ = protobuf_Topologys
        self.jinja2_env_ = jinja2_env

    def CreateBgpdConfigs(self):
        """Creates a list of bgp configs from the quagga_bgpd_template.j2 using the
        protobuf Host and Topology message type. Topology informs the neighbor quagga
        configuration lines and the host informs the router-id and router bgp lines
        It ignores HT_LOOKUP service type host

        Returns: a dict of hostname to configurations to be written to files

        """

        hostname_to_host_dict = {}
        for host_proto in self.protobuf_Hosts_:
            host_name = host_proto.host_name
            hostname_to_host_dict[host_name] = host_proto


        template = 'quagga_template.j2'
        bgpd_template = self.jinja2_env_.get_template(template)
        config_dict = {}
        # for each host proto in hosts, it should generate configs only if it
        # not hosttype lookupservice
        for host_proto in self.protobuf_Hosts_:
            if(host_proto.host_type == QuaggaTopo_pb2.HostType.Value('HT_LOOKUPSERVICE')):
                continue
            template_variable_dict = {}
            template_variable_dict['asn'] = host_proto.as_num
            template_variable_dict['ip'] = host_proto.ip
            self.HandleTopology(template_variable_dict, hostname_to_host_dict, host_proto)
            config_dict[host_proto.host_name]= bgpd_template.render(template_variable_dict)
        # print "CONIFG DICT after HANDLE TOPO ", config_dict['a1']
        return config_dict

    def HandleTopology(self, template_variable_dict, hostname_to_host_dict, host_proto):
        """Mutates the template variable dictionary for a given host based on the topology
        entry if one exists.

        Arguments:
           template_variable_dict: The configuration dictionary that will be used
            to render the configuration. Will be mutated
           hostname_to_host_dict: lookup table for accessing host_protos of other
            hosts. Will be used when using the adjacentnodenames as a lookupkey
           host_proto: the host configuration being generated. Used to figure
           out what primary_node_name should be keyed on in the adjacency list
        """
        if self.protobuf_Topologys_ == None:
            return
        #find the adjacent nodes to the host being configured
        #Topologies_[0] because there will only ever be 1 topology
        adjacent_nodes = []
        for adjacency_list_entry in self.protobuf_Topologys_[0].adjacency_list_entries:
            if adjacency_list_entry.primary_node_name == host_proto.host_name:
                for adjacent_node_name in adjacency_list_entry.adjacent_node_names:
                    adjacent_nodes.append(adjacent_node_name)
                break
        # for each adjacent node, find the corresponding hostproto and add it
        # to the neighbor list of dictionaries. Add it to the template_variable_dict at
        # the end
        neighbors = []
        # print 'adjacentnodes ', adjacent_nodes
        for adjacent_node in adjacent_nodes:
            neighbor_dict = {}
            adjacent_host_proto = hostname_to_host_dict[adjacent_node]
            adjacent_host_ip = adjacent_host_proto.ip
            adjacent_host_asn = adjacent_host_proto.as_num
            neighbor_dict['ip'] = adjacent_host_ip
            neighbor_dict['asn'] = adjacent_host_asn
            neighbors.append(neighbor_dict)
        template_variable_dict['neighbors'] = neighbors
        # print "CONIFG DICT FROM HANDLE TOPO ", template_variable_dict





