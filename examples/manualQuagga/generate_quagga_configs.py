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
        template = 'quagga_template.j2'
        bgpd_template = self.jinja2_env_.get_template(template)
        config_list = []
        for host_proto in self.protobuf_Hosts_:
            if(host_proto.host_type == QuaggaTopo_pb2.HostType.Value('HT_LOOKUPSERVICE')):
                continue
            template_variable_dict = {}
            template_variable_dict['asn'] = host_proto.as_num
            template_variable_dict['ip'] = host_proto.ip
            config_list.append(bgpd_template.render(template_variable_dict))
        return config_list

