import autonetkit
from autonetkit.compilers.device.quagga import QuaggaCompiler
from autonetkit.nidb.node import DmNode
from autonetkit.nidb.base import DmBase
from autonetkit.anm.node import NmNode
import autonetkit.console_script as console_script
import autonetkit.render as render






if __name__ == '__main__':
    anm = autonetkit.NetworkModel()
    bgp_overlay = anm.add_overlay('ebgp_v4')
    ipv4_overlay = anm.add_overlay('ipv4')
    phy_overlay = anm.overlay('phy')


    nm_node = NmNode(anm, 'ebgp_v4', 'nodetest')
    phy_overlay.add_node(nm_node)
    ipv4_overlay.add_node(nm_node)
    bgp_overlay.add_node(nm_node)
    nidb = console_script.workflow.create_nidb(anm)
    node = nidb.node('nodetest')

    render.render_node(nidb.node('nodetest'))

    quagga_compiler = QuaggaCompiler(nidb, anm)
    # quagga_compiler.compile(nidb.node('nodetest'))

    print 'test'
