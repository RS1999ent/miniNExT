import unittest
import quagga_config_pb2
import jinja2
from generate_wiser_configs import GenerateWiserConfigs
from google.protobuf.text_format import Merge

class GenerateWiserConfigsTest(unittest.TestCase):

    def testXCreateBgpdConfigsXOneHostQuaggaTopoXOneNodeLinkWiserConfig(self):
        #arrange
        kHostList = [
            """
            host_type : HT_QUAGGA
            host_name : 'a1'
            ip : '192.168.1.1'
            lo_ip : '10.1.1.1'
            as_num : 100
            """
        ]
        kTopologyList = None

        kCorrectWiserConfigDict = {'a1' :
        """
        Topology {
        node_links {
        primary_node {
        node_name : 'a1'
        interface_ip : '192.168.1.1'
        }
        }
        }
        """
        }

        correct_dictionary = {}
        for hostname,text_proto in kCorrectWiserConfigDict:
            tmp_wiserprotocolconfig = quagga_config_pb2.WiserProtocolConfig()
            Merge(text_proto, tmp_wiserprotocolconfig)
            correct_dictionary[hostname] = tmp_wiserprotocolconfig.SerializeToString()
        Merge(kCorrectWiserConfig, correct_config)

        host_list = []
        for host_string in kHostList:
            tmp_host = QuaggaTopo_pb2.Host()
            host_list.append(Merge(host_string, tmp_host))


        generate_wiser_configs = GenerateWiserConfigs(host_list, None)

        #act
        result_configs_dict = generate_wiser_configs.CreateWiserConfigs()

        #assert
        self.assertDictEqual(correct_dictionary, result_configs_dict)
