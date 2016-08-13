import unittest
import quagga_config_pb2
import QuaggaTopo_pb2
from generate_wiser_configs import GenerateWiserConfigs
from google.protobuf.text_format import Merge

class GenerateWiserConfigsTest(unittest.TestCase):

    #TODO: check if hosttype is quagga (todo). Test with a topology (todo)
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
        topology {
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
        for hostname,text_proto in kCorrectWiserConfigDict.iteritems():
            tmp_wiserprotocolconfig = quagga_config_pb2.WiserProtocolConfig()
            Merge(text_proto, tmp_wiserprotocolconfig)
            correct_dictionary[hostname] = tmp_wiserprotocolconfig.SerializeToString()

        host_list = []
        for host_string in kHostList:
            tmp_host = QuaggaTopo_pb2.Host()
            host_list.append(Merge(host_string, tmp_host))


        generate_wiser_configs = GenerateWiserConfigs(host_list, None)

        #act
        result_configs_dict = generate_wiser_configs.CreateWiserConfigs()

        #serialize protos for equality checking
        assert_dict = {}
        for hostname, wiserprotocolconfig in result_configs_dict:
            assert_dict[hostname] = wiserprotocolconfig.SerializeToString()


        #assert
        self.assertDictEqual(correct_dictionary, assert_dict)

suite = unittest.TestLoader().loadTestsFromTestCase(GenerateWiserConfigsTest)
runner = unittest.TextTestRunner()
runner.run(suite)
