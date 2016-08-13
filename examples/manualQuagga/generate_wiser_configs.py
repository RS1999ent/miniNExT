import QuaggaTopo_pb2
import quagga_config_pb2

class GenerateWiserConfigs():
    """Class responsible for generating a list of configs that are later to be
written to a file. These configs are specific to the wiser protocol information
that quagga wants. The jinja2_env should contain: quagga_wiser_template.j2"""

    protobuf_hosts_ = None
    protobuf_topologys_ = None

    def __init__(self, protobuf_hosts, protobuf_topologys):
        """Just initialize class variables"""
        self.protobuf_hosts_ = protobuf_hosts
        self.protobuf_topologys_ = protobuf_topologys_
