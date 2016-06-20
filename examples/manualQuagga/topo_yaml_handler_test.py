import unittest
from topo_yaml_handler import TopoYamlHandler
# from topo_yaml_handler import HostStruct
import yaml


class TopoYamlHandlerTest(unittest.TestCase):
    topo_yaml_handler = None
    def setUp(self):
        self.topo_yaml_handler = TopoYamlHandler()
    def parseHostTypeYamlDoc_givenWellFormattedHostYamlDoc_ReturnStructWithFieldsFilledIn(self):
        kHostYaml = """
        type : HOST
        name: a1
        ip: 172.0.1.1/16
        lo_ip: 10.0.1.1/24
        """
        correctStruct = self.topo_yaml_handler.HostStruct(name='a1', ip='172.0.1.1/16', lo_ip = '10.0.1.1/24')
        # correctStruct.name = "a1";
        # correctStruct.ip = "172.0.1.1/16"
        # correctStruct.lo_ip = "10.0.1.1/24"

        yaml_input = yaml.load(kHostYaml)
        result_struct = self.topo_yaml_handler.parseHostTypeYamlDoc(yaml_input)

        self.assertEqual(correctStruct.name, result_struct.name)
        self.assertEqual(correctStruct.ip, result_struct.ip)
        self.assertEqual(correctStruct.lo_ip, result_struct.lo_ip)

    def parseHostTypeYamlDoc_givenWellFormattedHostYamlDocWithoutLoIp_ReturnStructWithFieldsFilledIn(self):
        kHostYaml = """
        type : HOST
        name: a1
        ip: 172.0.1.1/16
        """
        correctStruct = self.topo_yaml_handler.HostStruct(name='a1', ip='172.0.1.1/16', lo_ip=None)

        yaml_input = yaml.load(kHostYaml)
        result_struct = self.topo_yaml_handler.parseHostTypeYamlDoc(yaml_input)


        self.assertEqual(correctStruct.name, result_struct.name)
        self.assertEqual(correctStruct.ip, result_struct.ip)
        self.assertEqual(correctStruct.lo_ip, result_struct.lo_ip)

    def parseTopologyTypeYamlDoc_givenWellFormattedTopoYamlDoc_ReturnDictionayofLists(self):
        # kTopoYaml = """
        # type : TOPOLOGY \
        # - a1 \
        #   - b1 \
        # - b1 \
        #   - a1 \
        # """
        kTopoYaml = """
        type : TOPOLOGY
        adjacency_list:
        - a1: [b1]
        - b1: [a1]
        """
        kCorrectResult = {'a1': ['b1'], 'b1': ['a1']}

        input_yaml = yaml.load(kTopoYaml)
        result = self.topo_yaml_handler.parseTopologyTypeYamlDoc(input_yaml)

        self.assertEqual(result, kCorrectResult)

    def handleTYpedYamlDocument_givenWellFormattedTopoYamlDoc_classAdjListIsCorrect(self):
        # kTopoYaml = """
        # type : TOPOLOGY \
        # - a1 \
        #   - b1 \
        # - b1 \
        #   - a1 \
        # """
        kTopoYaml = """
        type : TOPOLOGY
        adjacency_list:
        - a1: [b1]
        - b1: [a1]
        """
        kCorrectResult = {'a1': ['b1'], 'b1': ['a1']}

        input_yaml = yaml.load(kTopoYaml)
        self.topo_yaml_handler.handleTypedYamlDocument(input_yaml)

        self.assertEqual(self.topo_yaml_handler.adjacency_list, kCorrectResult)

    def handleTypedYamlDocument_givenWellFormattedHostYamlDoc_ReturnStructWithFieldsFilledIn(self):
        kHostYaml = """
        type : HOST
        name: a1
        ip: 172.0.1.1/16
        lo_ip: 10.0.1.1/24
        """
        correctStruct = self.topo_yaml_handler.HostStruct(name='a1', ip='172.0.1.1/16', lo_ip='10.0.1.1/24')

        yaml_input = yaml.load(kHostYaml)
        self.topo_yaml_handler.handleTypedYamlDocument(yaml_input)

        result_struct = self.topo_yaml_handler.hosts_list[0]

        self.assertEqual(correctStruct.name, result_struct.name)
        self.assertEqual(correctStruct.ip, result_struct.ip)
        self.assertEqual(correctStruct.lo_ip, result_struct.lo_ip)




