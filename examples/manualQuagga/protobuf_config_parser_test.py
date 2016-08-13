import unittest
import QuaggaTopo_pb2
from protobuf_config_parser import ProtobufConfigParser
from StringIO import StringIO

class ProtobufConfigParserTest(unittest.TestCase):
    protobuf_config_parser = None
    def setUp(self):
        self.protobuf_config_parser = ProtobufConfigParser()
    def testparseProtobufConfig_givenConfigWithOneHostEntry_ClassDataStructHaveOneEntry(self):
        protobuf_config_parser = ProtobufConfigParser()
        kTestInput = """
        <begin Host>
        host_type : HT_QUAGGA
        ip: '192.168.1.1'
        lo_ip: '10.10.1.1'
        <end Host>
        """
        test_input = StringIO(kTestInput)
        protobuf_config_parser.parseProtobufConfig(test_input)
        self.assertEqual(len(protobuf_config_parser.protobuf_Hosts_), 1) 

    def testparseProtobufConfig_givenConfigWithOneBadFromatEntry_ClassDataStructHaveZeroEntry(self):
        kTestInput = """
        <begin Host>
        hosggt_type : HT_QUAGGA
        asdfip: '192.168.1.1'
        lo_ip: '10.10.1.1'
        <end Host>
        """
        test_input = StringIO(kTestInput)
        self.protobuf_config_parser.parseProtobufConfig(test_input)
        self.assertEqual(len(self.protobuf_config_parser.protobuf_Hosts_), 0)

    def testparseProtobufConfig_givenConfigWithOneTopologyEntry_ClassDataStructHaveOneEntry(self):
        kTestInput = """
        <begin Topology>
        adjacency_list_entries {
        primary_node_name: 'a1'
        links {
        adjacent_node_name : 'b1'
        }
        links {
        adjacent_node_name : 'c1'
        }
        }
        <end Topology>
        """
        test_input = StringIO(kTestInput)
        self.protobuf_config_parser.parseProtobufConfig(test_input)
        self.assertEqual(len(self.protobuf_config_parser.protobuf_Topologys_), 1) 


    def testparseProtobufConfig_givenConfigWithBadFormatTopologyEntry_ClassDataStructHaveZeroEntry(self):
        kTestInput = """
        <begin Topology>
        afdjacency_list_entries {
        prgsdgjimary_node_name: 'a1'
        adjacent_node_names : 'b1'
        adjacent_node_names : 'c1'
        }
        <end Topology>
        """
        test_input = StringIO(kTestInput)
        self.protobuf_config_parser.parseProtobufConfig(test_input)
        self.assertEqual(len(self.protobuf_config_parser.protobuf_Topologys_), 0)


    def testparseProtobufConfig_givenConfigWithMultiEntry_ClassDataStructHaveOneEntryInEachDataStructure(self):
        kTestInput = """
        <begin Host>
        ip : '19.19.19.1'
        <end Host>
        <begin Topology>
        adjacency_list_entries {
        primary_node_name: 'a1'
        links {
        adjacent_node_name : 'b1'
        }
        links {
        adjacent_node_name : 'c1'
        }
        }
        <end Topology>
        """
        test_input = StringIO(kTestInput)
        self.protobuf_config_parser.parseProtobufConfig(test_input)
        self.assertEqual(len(self.protobuf_config_parser.protobuf_Topologys_), 1)
        self.assertEqual(len(self.protobuf_config_parser.protobuf_Hosts_), 1)


# suite = unittest.TestLoader().loadTestsFromTestCase(ProtobufConfigParserTest)
# runner = unittest.TextTestRunner()
# runner.run(suite)
