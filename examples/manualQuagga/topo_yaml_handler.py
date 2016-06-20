import yaml
from collections import namedtuple


class TopoYamlHandler():
    """Handles parsing into relevent data structures the YAML file describing the
    quagga topology"""
    HostStruct = namedtuple("HostStruct", "name ip lo_ip")
    hosts_list = []
    adjacency_list = {}

    def __init__(self):
        flie_name = None

        """Parses a yaml document that is in host type format and return
        HostStruct named tuple
        Format:
            type: <string>
            name : <string>
            ip : <string>
            lo_ip: <string> (optional)
         """
    def parseHostTypeYamlDoc(self, yaml_document):
        # return_struct = HostStruct()

        # Extract relevent fields
        name = yaml_document["name"]
        ip = yaml_document["ip"]
        lo_ip = None

        #lo ip is optional
        if "lo_ip" in yaml_document:
            lo_ip = yaml_document["lo_ip"]
        return self.HostStruct(name, ip, lo_ip)
    """Takes in a topology type yaml document and returns dictionary of format
<'nodename', <list of nodenames adjacent>>
    Topology format is:
    type: TOPOLOGY
    - a1 : [b1, b2, b3]
    - b2 : [a1, a2, a4]
    .
    .
    .
    """
    def parseTopologyTypeYamlDoc(self, yaml_document):
        return_dictionary = {}

        for node in yaml_document:
            #skip the type descriminator of the document
            if node == 'type':
                continue
            if node == 'adjacency_list':
                # Each entry is of type {'nodename' : [adjacentnodes]} since we
                #know that there is only one key in this entry, we get the [0]
                #of the keys of the dictionary, same logic with the values, we
                #know there is a single list so we get the first one
                for node_with_adjacency_list in yaml_document[node]:
                    return_dictionary[node_with_adjacency_list.keys()[0]] =  node_with_adjacency_list.values()[0]
            return return_dictionary

    """Takes in a yaml_ocument with type entry and fills in class datastructures"""
    def handleTypedYamlDocument(self, yaml_document):
        if yaml_document['type'] == 'HOST':
            self.hosts_list.append(self.parseHostTypeYamlDoc(yaml_document))
        if yaml_document['type'] == 'TOPOLOGY':
            self.adjacency_list = self.parseTopologyTypeYamlDoc(yaml_document)

    def parseYamlFile(self, file_name):
        """Takes in an existing file name and parses the yaml documents within and filling the class data structures.
        NO UNIT TEST, no special logic for non existent files
        """
        yaml_stream = open(file_name, 'r')
        for document in yaml.load_all(yaml_stream):
            self.handleTypedYamlDocument(document)


def main():
    topo_handler = TopoYamlHandler()
    topo_handler.parseYamlFile('QuaggaTopo.yml')
    print topo_handler.hosts_list
    print topo_handler.adjacency_list

if __name__ == '__main__':
    main()
