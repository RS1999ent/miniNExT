import QuaggaTopo_pb2
from google.protobuf.text_format import Merge
from StringIO import StringIO
import re
class ProtobufConfigParser():
    """Class responsible for parsing a protobuf config file into the list of the
    protobuf datastructs"""

    # list of Host protobufs datastructs
    protobuf_Hosts_ = []

    #list of Topology protobuf datastructs
    protobuf_Topologys_ = []

    def parseProtobufConfig(self, open_file_handle):
        """ Goes through passed file and parses it into the various protobuf
        datastructures Class lists that will be mutated will be the protobuf_.*
        with the protobuf messages added to each correspond to the type listed
        in the variable name

        Arguments:
           open_file_handle: Valid open file containing the protobuf datastructs in text format
        """

        message_type = ''
        protobuf_message = ''
        for line in open_file_handle:
            #extract the individual protobuf messages of currently unknown type
            if re.search('<begin\ \w+>', line):
                protobuf_message = ''
                #split on the space, then the type is the second element minus
                #the '>'
                message_type = line.split()[1][:-1]
            #end of message, parse it into datastructures
            elif re.search('<end\ \w+>', line):
                if(self.ParseProtoMessageIntoDataStructs(protobuf_message, message_type) == -1):
                    print "Parse Error of message of type: ", message_type, protobuf_message
            else:
                protobuf_message += line

    def ParseProtoMessageIntoDataStructs(self, message, message_type):
        """ Taken a protobuf message in string format and its type, parses it into the
        proper class datastructure holding the protobuf
        Arugments:
           message: the text formatted protbuf message to be parsed.
           message_type: string telling us the protbuf type. Ex. 'Host' means Host protubf type
        Returns: -1 on either parse error or no type defined error, 1 otherwise
        """
        if message_type == 'Host':
            new_host = QuaggaTopo_pb2.Host()
            try:
                Merge(message, new_host)
            except Exception:
                return -1
            # Merge(message, new_host)
            self.protobuf_Hosts_.append(new_host)
            return 1
        if message_type == 'Topology':
            new_topology = QuaggaTopo_pb2.Topology()
            try:
                Merge(message, new_topology)
            except Exception:
                return -1
            self.protobuf_Topologys_.append(new_topology)
            return 1
        return -1




