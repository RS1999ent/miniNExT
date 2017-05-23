
0)apt-get install mininet.  Make sure it is version 2.1

1)Clone MiniNeXt and build it.

2)Cd to examples/manualQuagga

3)sudo start.py to start mininet with a default config, which is
'protobufconfig' in examples/manualQuagga.

start.py commandline:
         -f/--protobuf_config_file - name of file in current
         directoy or fully qualified path to file that contains the configuration in
         protobuf text format. By default, it uses the file named "protobufconfig" if
         this isn't specified
         -c/--predone_bgpdconfig - If 1, this means that the bgpd configs are
          already predone and shouldn't be generated from the protobufconfig
          -d/--delete_configs - If 1, then we want to delete the config tree
           that was created

         -h - displays helpline for commandline options

Configuration format:

Each top level message is demarcated by a <begin ''messagetype''> ... <end ''messagetype''>
Host config example:
<begin Host>
host_type : HT_QUAGGA
host_name: "b1"
ip: "172.0.2.1"
lo_ip: "10.0.2.1"
as_num: 101
path_to_initd: ".../quagga/initd_script"
<end Host>

Defines the protobuf text format for a 'Host' message type and will be parsed
into a host protobuf message. 'path_to_initd' is optional and specifies a
particular initd script to be run. Otherwise, uses the default on the system.

Topology config example:
<begin Topology>
adjacency_list_entries {
    primary_node_name: "a1"
    links{
        adjacent_node_name: "b1"
        link_cost : 10
    }
}
adjacency_list_entries {
    primary_node_name: "b1"
    links{
        adjacent_node_name: "a1"
        link_cost: 10
    }
}
<end Topology>

This defines a protobuf topology message in text format.

NOTE1: while it looks like you can have asymetric link costs, when quagga is
running, it is assuming that costs are symetric. Therefore, if you define
asymetric costs, the behavior is undefined.

NOTE2: For the purposes of configuration in MiniNext, you have to define both
ends of the link. That is, a link from a1 to b1 has to be defined like above
(one from a1 to b1 and one from b1 to a1).

An example of defining a redis host is:
<begin Host>
host_type : HT_LOOKUPSERVICE
host_name: "l1"
ip: "172.1.1.1"
path_to_executable : "redis-server"
<end Host>

'path_to_executable' is the command that will start redis-server relative from root.
The ip should be the wellknown ip that is defined in quagga.

Each message specification is defined by the protobuf, QuaggaTopo.proto. See
the file "protobufconfig" for an example configuation. See documentation in
QuaggaTopo.proto for more information.

Required fields:

While all fields are defined as 'optional' in the proto, you should fill in all
fields related to the type of thing being defined otherwise undefined behavior
may occur.

host requird fields:
host_type : REQUIRED for all hosts
host_name : REQUIRED for all hosts
ip : REQUIRED for all hosts
lo_ip : REQUIRED for HT_QUAGGA hosts
as_num : REQUIRED for HT_QUAGGA hosts
path_to_redis : REQUIRED for HT_LOOKUPSERVICE hosts

topology requird fields:
each adjacentcy_list_entries should have a primary_node_name and at least one
"links" and each "links" must have an 'adjacent_node_name' and 'link_cost'

Dependencies:
Runs with python 2.7
libprotoc 2.6.1
protobuf-compiler
python-protobuf

The following commands should build python libraries.
pip install jinja2
pip install protobuf

BELOW IS THE README FROM THE MASTER MININEXT REPO

miniNExT
==============

MiniNExT (_Mininet ExTended_) is an extension layer that makes it easier to build complex networks in [Mininet](http://www.mininet.org).

**MiniNExT does not currently support the latest version of Mininet -- you must use version 2.1.0**

MiniNExT includes building blocks that are used in many experimental networks, including:

* Routing engines (Quagga and BIRD)
* Servers (BIND and Apache)
* Connectivity components (OpenVPN, etc.)
* NAT and Network Management components (DHCP, etc.)

In addition, MiniNExT hosts / containers can provide greater isolation, including:

* PID namespaces - isolates each container's processes, improving application support and analysis
* UTS namespaces - each host can have its own hostname, simplifying debugging and analysis
* Improved mount namespaces - makes it possible to override each host's view of their local filesystem 
* Log and runtime isolation - each host can have its own /var/log and /run with one line

We also make it easier to express common configurations with:

* Service helpers - makes it easier to run and manage the services in your hosts
* Network helpers - makes it easier to configure loopback interfaces and NAT networks
* Mount management - makes it easier to provide hosts with individual application configurations

We hope to upstream some of these extensions (such as support for PID and UTS namespaces, easier mount management, etc.) into mainline Mininet.

## Project Details

MiniNExT was developed by Brandon Schlinker at [The University of Southern California](http://www.usc.edu) in collaboration with Kyriakos Zarifis (USC), Italo Cunha (UFMG), Nick Feamster (GaTech), Ethan Katz-Bassett (USC), and Minlan Yu (USC).

MiniNExT is part of the PEERING project at USC, which combines Transit Portal and MiniNExT. Combined, these tools enable researchers to build realistic AS topologies that can exchange BGP routes and traffic with _real_ ISPs around the world. The PEERING tools played a role in evaluating [Software Defined Internet Exchanges](http://noise-lab.net/projects/software-defined-networking/sdx/) by making it possible to build a virtual IXP fabric composed of _real_ ISP peers.

For problems with the code base, please use the GitHub issue tracker. All other queries, please email bschlink@usc.edu

## Getting Started

### Installing Mininet

MiniNExT depends on the Mininet software package, and thus you must have Mininet installed.

**MiniNExT does not currently support the latest version of Mininet -- you must use version 2.1.0**

You can check if you already have Mininet installed and its version by executing `mn --version`

You can install Mininet version 2.1.0 on Ubuntu by executing:
```
$ sudo apt-get install mininet=2.1.0-0ubuntu1
```

If the above fails, you may need to uninstall your current version of Mininet:
```
$ sudo apt-get purge mininet
```

You can also check if your package manager has Mininet version 2.1.0:
```
$ sudo apt-cache madison ^mininet
```

Alternatively, Mininet can be installed from source by following the instructions on the [Mininet website](http://www.mininet.org)

### Downloading MiniNExT

MiniNExT sources are available [here](http://mininext.uscnsl.net). The easiest option is to download a `.zip` or `.tar.gz` source archive. Download and extract the archive to a location in your home directory.

You may also prefer to use `git` to `clone` the MiniNExT repository to make upgrading easier.

### Installing MiniNExT Dependencies

MiniNExT depends on a packages that may not be installed by default with Mininet.

To list these dependencies, execute the following in the directoy where you _extracted_ MiniNExT:
```
$ make deps
```

These dependencies can be installed on Debian/Ubuntu by executing:
```
$ sudo apt-get install `make deps`
```

### Installing MiniNExT

To install MiniNExT, execute the following in the directoy where you _extracted_ MiniNExT:
```
$ sudo make install
```

### Uninstalling MiniNExT

To uninstall MiniNExT, execute the following in the directoy where you _extracted_ MiniNExT:
```
$ sudo make uninstall
```

Note that the `pip` package must be installed for this to work.

### Developer Installation

If you're extending or debugging MiniNExT, you likely do _not_ want to install to the system's Python library. 

Instead, you can run the following command to install MiniNExT in developer mode:
```
$ sudo make develop
```

This triggers the [development mode](https://pythonhosted.org/setuptools/setuptools.html#development-mode) that is provided by the `setuptools` package, which then creates a link instead of performing a complete installation. However, note that the `mxexec` and supporting help files are still installed into their respective system paths.

To remove, run:
```
$ sudo make undevelop
```


**Note:** MiniNExT no longer _forks_ Mininet<br>
Previously MiniNExT functionality was built by forking and modifying the original Mininet source code. However, this created conflicts with existing Mininet installations and made it difficult to merge in upstream changes. MiniNExT has been redesigned to _extend_ Mininet, and does _not_ impact default Mininet execution.
