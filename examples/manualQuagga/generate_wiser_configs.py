import QuaggaTopo_pb2
import jinja2

class GenerateWiserConfigs():
    """Class responsible for generating a list of configs that are later to be
written to a file. These configs are specific to the wiser protocol information
that quagga wants. The jinja2_env should contain: quagga_wiser_template.j2"""

    protobuf_hosts_ = None
    protobuf_topologys_ = None
    jinja2_env_ = None

    def __init__(self, protobuf_hosts, protobuf_topologys, jinja2_env):
        """Just initialize class variables"""
        self.protobuf_hosts_ = protobuf_hosts
        self.protobuf_topologys_ = protobuf_topologys_
        self.jinja2_env_ = jinja2_env
