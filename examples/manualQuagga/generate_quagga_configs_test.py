import unittest
import QuaggaTopo_pb2
import jinja2
from generate_quagga_configs import GenerateQuaggaConfigs
from google.protobuf.text_format import Merge

class GenerateQuaggaConfigsTest(unittest.TestCase):
    kBgpdTemplate = """
    ! path logfile for this daemon (BGPD)
    log file /var/log/quagga/bgpd.log

    ! the password to use for telnet authentication
    password bgpuser

    ! this routers AS number and BGP ID
    router bgp {{ asn }}
    bgp router-id {{ ip }}

    {% for neighbor in neighbors %}
    neighbor {{ neighbor.ip }} remote-as {{ neighbor.as }}
    {% endfor %}

    ! the network this router will advertise
    ! network 10.0.1.0/24
    """
    jinja2_env_ = None
    def setUp(self):
                self.jinja2_env_ = jinja2.Environment(loader=jinja2.DictLoader({'quagga_template.j2' : self.kBgpdTemplate}))

    def testCreateBgpdConfigs_GivenOneHost_OneStringConfigReturned(self):
        kCorrectOutput = """
        ! path logfile for this daemon (BGPD)
        log file /var/log/quagga/bgpd.log

        ! the password to use for telnet authentication
        password bgpuser

        ! this routers AS number and BGP ID
        router bgp 100
        bgp router-id 192.168.1.1

        {% for neighbor in neighbors %}
        neighbor {{ neighbor.ip }} remote-as {{ neighbor.as }}
        {% endfor %}

        ! the network this router will advertise
        ! network 10.0.1.0/24
        """

        kCorrectOutput = '\n    ! path logfile for this daemon (BGPD)\n    log file /var/log/quagga/bgpd.log\n\n    ! the password to use for telnet authentication\n    password bgpuser\n\n    ! this routers AS number and BGP ID\n    router bgp 100\n    bgp router-id 192.168.1.1\n\n    \n\n    ! the network this router will advertise\n    ! network 10.0.1.0/24\n    '

        kHost1 = """
        host_type : HT_QUAGGA
        ip: '192.168.1.1'
        lo_ip: '10.10.1.1'
        as_num: 100
        """
        host_list = []
        tmp_host = QuaggaTopo_pb2.Host()
        host_list.append(Merge(kHost1, tmp_host))
        self.generate_quagga_configs_ = GenerateQuaggaConfigs(host_list, None, self.jinja2_env_)

        result_configs_list = self.generate_quagga_configs_.CreateBgpdConfigs()
        self.assertEquals(result_configs_list[0], kCorrectOutput)


    def testCreateBgpdConfigs_GivenTwoHost_TwoStringConfigReturned(self):
        kCorrectOutputHost1 = """
        ! path logfile for this daemon (BGPD)
        log file /var/log/quagga/bgpd.log

        ! the password to use for telnet authentication
        password bgpuser

        ! this routers AS number and BGP ID
        router bgp 100
        bgp router-id 192.168.1.1

        {% for neighbor in neighbors %}
        neighbor {{ neighbor.ip }} remote-as {{ neighbor.as }}
        {% endfor %}

        ! the network this router will advertise
        ! network 10.0.1.0/24
        """

        kCorrectOutputHost1 = '\n    ! path logfile for this daemon (BGPD)\n    log file /var/log/quagga/bgpd.log\n\n    ! the password to use for telnet authentication\n    password bgpuser\n\n    ! this routers AS number and BGP ID\n    router bgp 100\n    bgp router-id 192.168.1.1\n\n    \n\n    ! the network this router will advertise\n    ! network 10.0.1.0/24\n    '

        kCorrectOutputHost2 = '\n    ! path logfile for this daemon (BGPD)\n    log file /var/log/quagga/bgpd.log\n\n    ! the password to use for telnet authentication\n    password bgpuser\n\n    ! this routers AS number and BGP ID\n    router bgp 101\n    bgp router-id 192.168.1.2\n\n    \n\n    ! the network this router will advertise\n    ! network 10.0.1.0/24\n    '

        kHost1 = """
        host_type : HT_QUAGGA
        ip: '192.168.1.1'
        lo_ip: '10.10.1.1'
        as_num: 100
        """
        kHost2 = """
        host_type : HT_QUAGGA
        ip: '192.168.1.2'
        lo_ip: '10.10.1.2'
        as_num: 101
        """
        host_list = []
        tmp_host = QuaggaTopo_pb2.Host()
        host_list.append(Merge(kHost1, tmp_host))
        tmp_host = QuaggaTopo_pb2.Host()
        host_list.append(Merge(kHost2, tmp_host))



        self.generate_quagga_configs_ = GenerateQuaggaConfigs(host_list, None, self.jinja2_env_)

        result_configs_list = self.generate_quagga_configs_.CreateBgpdConfigs()
        self.assertEquals(result_configs_list[0], kCorrectOutputHost1)
        self.assertEquals(result_configs_list[1], kCorrectOutputHost2)


    def testCreateBgpdConfigs_GivenTwoHostWithOneOfThemBeingATypeLookUpService_OneStringConfigReturned(self):
        kCorrectOutputHost1 = """
        ! path logfile for this daemon (BGPD)
        log file /var/log/quagga/bgpd.log

        ! the password to use for telnet authentication
        password bgpuser

        ! this routers AS number and BGP ID
        router bgp 100
        bgp router-id 192.168.1.1

        {% for neighbor in neighbors %}
        neighbor {{ neighbor.ip }} remote-as {{ neighbor.as }}
        {% endfor %}

        ! the network this router will advertise
        ! network 10.0.1.0/24
        """

        kCorrectOutputHost1 = '\n    ! path logfile for this daemon (BGPD)\n    log file /var/log/quagga/bgpd.log\n\n    ! the password to use for telnet authentication\n    password bgpuser\n\n    ! this routers AS number and BGP ID\n    router bgp 100\n    bgp router-id 192.168.1.1\n\n    \n\n    ! the network this router will advertise\n    ! network 10.0.1.0/24\n    '

        kHost1 = """
        host_type : HT_QUAGGA
        ip: '192.168.1.1'
        lo_ip: '10.10.1.1'
        as_num: 100
        """
        kHost2 = """
        host_type : HT_LOOKUPSERVICE
        ip: '192.168.1.2'
        lo_ip: '10.10.1.2'
        as_num: 101
        """
        host_list = []
        tmp_host = QuaggaTopo_pb2.Host()
        host_list.append(Merge(kHost1, tmp_host))
        tmp_host = QuaggaTopo_pb2.Host()
        host_list.append(Merge(kHost2, tmp_host))

        self.generate_quagga_configs_ = GenerateQuaggaConfigs(host_list, None, self.jinja2_env_)

        result_configs_list = self.generate_quagga_configs_.CreateBgpdConfigs()
        self.assertEquals(result_configs_list[0], kCorrectOutputHost1)
        self.assertEquals(len(result_configs_list), 1)

suite = unittest.TestLoader().loadTestsFromTestCase(GenerateQuaggaConfigsTest)
runner = unittest.TextTestRunner()
runner.run(suite)
