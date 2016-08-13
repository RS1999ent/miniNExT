import unittest
import quagga_config_pb2
import QuaggaTopo_pb2
from generate_wiser_configs import GenerateWiserConfigs
from google.protobuf.text_format import Merge

class GenerateWiserConfigsTest(unittest.TestCase):

    #TODO: check if hosttype is quagga (testdone). Test with more than one host (todo) test with multilink multihost(todo)
    def testXCreateBgpdConfigsXOneHostQuaggaTopoXOneNodeLinkWiserConfig(self):
        #arrange
        kHostList = [
            """
            host_type : HT_QUAGGA
            host_name : 'a1'
            ip : '192.168.1.1'
            lo_ip : '10.1.1.1'
            as_num : 100"""
        ]
        kTopologyList = None

        kCorrectWiserConfigDict = {'a1' : ''
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
        for hostname, wiserprotocolconfig in result_configs_dict.iteritems():
            assert_dict[hostname] = wiserprotocolconfig.SerializeToString()


        #assert
        self.assertDictEqual(correct_dictionary, assert_dict)

    def testXCreateBgpdConfigsXOneHostNotQuaggaTopoXEmptyDict(self):
        #arrange
        kHostList = [
            """
            host_type : HT_LOOKUPSERVICE
            host_name : 'a1'
            ip : '192.168.1.1'
            lo_ip : '10.1.1.1'
            as_num : 100"""
        ]
        kTopologyList = None

        kCorrectWiserConfigDict = {
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
        for hostname, wiserprotocolconfig in result_configs_dict.iteritems():
            assert_dict[hostname] = wiserprotocolconfig.SerializeToString()


        #assert
        self.assertDictEqual(correct_dictionary, assert_dict)

    def testXCreateBgpdConfigsXTwoHostOneLinkXCorrectDict(self):
        #arrange
        kHostList = [
            """
            host_type : HT_QUAGGA
            host_name : 'a1'
            ip : '192.168.1.1'
            lo_ip : '10.1.1.1'
            as_num : 100""",
            """
            host_type : HT_QUAGGA
            host_name : 'b1'
            ip : '192.168.1.2'
            lo_ip : '10.1.1.2'
            as_num : 200"""
        ]
        kTopologyList = [
            """
            adjacency_list_entries {
            primary_node_name : 'a1'
            links {
            adjacent_node_name : 'b1'
            link_cost : 12
            }
            }
            adjacency_list_entries {
            primary_node_name : 'b1'
            links {
            adjacent_node_name : 'a1'
            link_cost : 12
            }
            }
            """

        ]

        kCorrectWiserConfigDict = {'a1' :
        """topology {
        node_links {
        primary_node {
        node_name : 'a1'
        interface_ip : '192.168.1.1'
        }
        links{
        adjacent_node {
        node_name : 'b1'
        interface_ip : '192.168.1.2'
        }
        link_cost : 12
        }
        }
        node_links {
        primary_node {
        node_name : 'b1'
        interface_ip : '192.168.1.2'
        }
        links{
        adjacent_node {
        node_name : 'a1'
        interface_ip : '192.168.1.1'
        }
        link_cost : 12
        }
        }
        }""",
        'b1' :"""
        topology {
        node_links {
        primary_node {
        node_name : 'a1'
        interface_ip : '192.168.1.1'
        }
        links{
        adjacent_node {
        node_name : 'b1'
        interface_ip : '192.168.1.2'
        }
        link_cost : 12
        }
        }
        node_links {
        primary_node {
        node_name : 'b1'
        interface_ip : '192.168.1.2'
        }
        links{
        adjacent_node {
        node_name : 'a1'
        interface_ip : '192.168.1.1'
        }
        link_cost : 12
        }
        }
        }"""

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

        topo_list = []
        for topo_string in kTopologyList:
            tmp_topo = QuaggaTopo_pb2.Topology()
            topo_list.append(Merge(topo_string, tmp_topo))


        generate_wiser_configs = GenerateWiserConfigs(host_list, topo_list)

        #act
        result_configs_dict = generate_wiser_configs.CreateWiserConfigs()

        #serialize protos for equality checking
        assert_dict = {}
        for hostname, wiserprotocolconfig in result_configs_dict.iteritems():
            assert_dict[hostname] = wiserprotocolconfig.SerializeToString()


        #assert
        self.assertDictEqual(correct_dictionary, assert_dict)
            
    def testXCreateBgpdConfigsXThreeHostTwoLinkXCorrectDict(self):
        #arrange
        kHostList = [
            """
            host_type : HT_QUAGGA
            host_name : 'a1'
            ip : '192.168.1.1'
            lo_ip : '10.1.1.1'
            as_num : 100""",
            """
            host_type : HT_QUAGGA
            host_name : 'b1'
            ip : '192.168.1.2'
            lo_ip : '10.1.1.2'
            as_num : 200""",
            """
            host_type : HT_QUAGGA
            host_name : 'c1'
            ip : '192.168.1.3'
            lo_ip : '10.1.1.3'
            as_num : 300"""

        ]
        kTopologyList = [
            """
            adjacency_list_entries {
            primary_node_name : 'a1'
            links {
            adjacent_node_name : 'b1'
            link_cost : 12
            }
            links {
            adjacent_node_name : 'c1'
            link_cost : 22
            }
            }
            adjacency_list_entries {
            primary_node_name : 'b1'
            links {
            adjacent_node_name : 'a1'
            link_cost : 12
            }
            }
            """
        ]

        kCorrectWiserConfigDict = {'a1' :
        """topology {
        node_links {
        primary_node {
        node_name : 'a1'
        interface_ip : '192.168.1.1'
        }
        links{
        adjacent_node {
        node_name : 'b1'
        interface_ip : '192.168.1.2'
        }
        link_cost : 12
        }
        links{
        adjacent_node {
        node_name : 'c1'
        interface_ip : '192.168.1.3'
        }
        link_cost : 22
        }
        }
        node_links {
        primary_node {
        node_name : 'b1'
        interface_ip : '192.168.1.2'
        }
        links{
        adjacent_node {
        node_name : 'a1'
        interface_ip : '192.168.1.1'
        }
        link_cost : 12
        }
        }
        }""",
        'b1' :
        """topology {
        node_links {
        primary_node {
        node_name : 'a1'
        interface_ip : '192.168.1.1'
        }
        links{
        adjacent_node {
        node_name : 'b1'
        interface_ip : '192.168.1.2'
        }
        link_cost : 12
        }
        links{
        adjacent_node {
        node_name : 'c1'
        interface_ip : '192.168.1.3'
        }
        link_cost : 22
        }
        }
        node_links {
        primary_node {
        node_name : 'b1'
        interface_ip : '192.168.1.2'
        }
        links{
        adjacent_node {
        node_name : 'a1'
        interface_ip : '192.168.1.1'
        }
        link_cost : 12
        }
        }
        }""",
        'c1' :
        """topology {
        node_links {
        primary_node {
        node_name : 'a1'
        interface_ip : '192.168.1.1'
        }
        links{
        adjacent_node {
        node_name : 'b1'
        interface_ip : '192.168.1.2'
        }
        link_cost : 12
        }
        links{
        adjacent_node {
        node_name : 'c1'
        interface_ip : '192.168.1.3'
        }
        link_cost : 22
        }
        }
        node_links {
        primary_node {
        node_name : 'b1'
        interface_ip : '192.168.1.2'
        }
        links{
        adjacent_node {
        node_name : 'a1'
        interface_ip : '192.168.1.1'
        }
        link_cost : 12
        }
        }
        }"""
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

        topo_list = []
        for topo_string in kTopologyList:
            tmp_topo = QuaggaTopo_pb2.Topology()
            topo_list.append(Merge(topo_string, tmp_topo))


        generate_wiser_configs = GenerateWiserConfigs(host_list, topo_list)

        #act
        result_configs_dict = generate_wiser_configs.CreateWiserConfigs()

        #serialize protos for equality checking
        assert_dict = {}
        for hostname, wiserprotocolconfig in result_configs_dict.iteritems():
            print hostname, wiserprotocolconfig.__str__()
            assert_dict[hostname] = wiserprotocolconfig.SerializeToString()


        #assert
        self.assertDictEqual(correct_dictionary, assert_dict)

suite = unittest.TestLoader().loadTestsFromTestCase(GenerateWiserConfigsTest)
runner = unittest.TextTestRunner()
runner.run(suite)
