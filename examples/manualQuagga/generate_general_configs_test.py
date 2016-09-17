import unittest
import quagga_config_pb2
import QuaggaTopo_pb2
from generate_general_configs import CreateGeneralConfigs
from google.protobuf.text_format import Merge

class GenerateGeneralConfigsTest(unittest.TestCase):
    def testxCreateGeneralConfigsXOneHostXCorrectConfigDict(self):
        #arrange
        kHostList = [
            """
            host_type : HT_QUAGGA
            host_name: 'a1'
            ip: '172.0.1.1'
            lo_ip: '10.0.1.1'
            as_num: 100
            island_id : 1
            protocol: 'wiser'
            """
        ]
        kTopology = """"""
        kCorrectGeneralConfigDict = {
            'a1' : """
            protocol_type : PT_WISER
            island_id : 1
            wiser_protocol_config {}
        """
        }

        correct_dictionary = {}
        for hostname,text_proto in kCorrectGeneralConfigDict.iteritems():
            tmp_generalprotocolconfig = quagga_config_pb2.Configuration()
            Merge(text_proto, tmp_generalprotocolconfig)
            correct_dictionary[hostname] = tmp_generalprotocolconfig.SerializeToString()

        host_list = []
        for host_string in kHostList:
            tmp_host = QuaggaTopo_pb2.Host()
            host_list.append(Merge(host_string, tmp_host))

        topology = QuaggaTopo_pb2.Topology()
        Merge(kTopology, topology)

        generate_wiser_configs = (host_list, topology)

        #act
        result_configs_dict = CreateGeneralConfigs(host_list, topology)

        #serialize protos for equality checking
        assert_dict = {}
        for hostname, generalprotocolconfig in result_configs_dict.iteritems():
            assert_dict[hostname] = generalprotocolconfig.SerializeToString()

        #assert
        self.assertDictEqual(correct_dictionary, assert_dict)

    def testxCreateGeneralConfigsXOneHostXCorrectConfigDict(self):
        #arrange
        kHostList = [
            """
            host_type : HT_QUAGGA
            host_name: 'a1'
            ip: '172.0.1.1'
            lo_ip: '10.0.1.1'
            as_num: 100
            island_id : 1
            protocol: 'wiser'
            """,
            """
            host_type : HT_QUAGGA
            host_name: 'b1'
            ip: '172.0.1.1'
            lo_ip: '10.0.1.1'
            as_num: 200
            island_id : 1
            protocol: 'wiser'
            """
        ]
        kTopology = """"""
        kCorrectGeneralConfigDict = {
            'a1' : """
            protocol_type : PT_WISER
            island_id : 1
            island_member_ases : 200
            wiser_protocol_config {}
            """,
            'b1' : """
            protocol_type : PT_WISER
            island_id : 1
            island_member_ases : 100
            wiser_protocol_config {}
        """
        }

        correct_dictionary = {}
        for hostname,text_proto in kCorrectGeneralConfigDict.iteritems():
            tmp_generalprotocolconfig = quagga_config_pb2.Configuration()
            Merge(text_proto, tmp_generalprotocolconfig)
            correct_dictionary[hostname] = tmp_generalprotocolconfig.SerializeToString()

        host_list = []
        for host_string in kHostList:
            tmp_host = QuaggaTopo_pb2.Host()
            host_list.append(Merge(host_string, tmp_host))

        topology = QuaggaTopo_pb2.Topology()
        Merge(kTopology, topology)

        generate_wiser_configs = (host_list, topology)

        #act
        result_configs_dict = CreateGeneralConfigs(host_list, topology)

        #serialize protos for equality checking
        assert_dict = {}
        for hostname, generalprotocolconfig in result_configs_dict.iteritems():
            assert_dict[hostname] = generalprotocolconfig.SerializeToString()




        #assert
        self.assertDictEqual(correct_dictionary, assert_dict)



suite = unittest.TestLoader().loadTestsFromTestCase(GenerateGeneralConfigsTest)
runner = unittest.TextTestRunner()
runner.run(suite)
