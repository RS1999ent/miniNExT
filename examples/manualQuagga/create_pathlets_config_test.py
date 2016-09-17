import unittest
import quagga_config_pb2
import QuaggaTopo_pb2
from create_pathlets_config import CreatePathletsConfig
from google.protobuf.text_format import Merge

class CreatePathletsConfigTest(unittest.TestCase):

    def testXCreatePathletsConfigXHostWOloIpXGetRightPathletBAck(self):
        # arrange
        kHostList = [
            """
            host_type : HT_QUAGGA
            host_name : 'a1'
            ip : '192.168.1.1'
            as_num : 100
            private_pathlet_ip : '192.168.1.1'
            is_border_router : 1
            """
        ]

        kCorrectPathletConfigDict = {'a1' :
                                     """ is_island_border_router: 1
                                     private_slash24_ip: '192.168.1.1'
                                     """
        }

        correct_dictionary = {}
        for hostname,text_proto in kCorrectPathletConfigDict.iteritems():
            tmp_pathletprotocolconfig = quagga_config_pb2.PathletProtoConfig()
            Merge(text_proto, tmp_pathletprotocolconfig)
            correct_dictionary[hostname] = tmp_pathletprotocolconfig.SerializeToString()

        host_list = []
        for host_string in kHostList:
            tmp_host = QuaggaTopo_pb2.Host()
            host_list.append(Merge(host_string, tmp_host))

        #act
        result_configs_dict = CreatePathletsConfig(host_list)

        #serialize protos for equality checking
        assert_dict = {}
        for hostname, pathletsprotocolconfig in result_configs_dict.iteritems():
            assert_dict[hostname] = pathletsprotocolconfig.SerializeToString()


        #assert
        self.assertDictEqual(correct_dictionary, assert_dict)

    def testXCreatePathletsConfigXHostNoBorderRouterIpXGetRightPathletBAck(self):
        # arrange
        kHostList = [
            """
            host_type : HT_QUAGGA
            host_name : 'a1'
            ip : '192.168.1.1'
            as_num : 100
            private_pathlet_ip : '192.168.1.1'
            """
        ]

        kCorrectPathletConfigDict = {'a1' :
                                     """ is_island_border_router: 0
                                     private_slash24_ip: '192.168.1.1'
                                     """
        }

        correct_dictionary = {}
        for hostname,text_proto in kCorrectPathletConfigDict.iteritems():
            tmp_pathletprotocolconfig = quagga_config_pb2.PathletProtoConfig()
            Merge(text_proto, tmp_pathletprotocolconfig)
            correct_dictionary[hostname] = tmp_pathletprotocolconfig.SerializeToString()

        host_list = []
        for host_string in kHostList:
            tmp_host = QuaggaTopo_pb2.Host()
            host_list.append(Merge(host_string, tmp_host))

        #act
        result_configs_dict = CreatePathletsConfig(host_list)

        #serialize protos for equality checking
        assert_dict = {}
        for hostname, pathletsprotocolconfig in result_configs_dict.iteritems():
            assert_dict[hostname] = pathletsprotocolconfig.SerializeToString()


        #assert
        self.assertDictEqual(correct_dictionary, assert_dict)



suite = unittest.TestLoader().loadTestsFromTestCase(CreatePathletsConfigTest)
runner = unittest.TextTestRunner()
runner.run(suite)