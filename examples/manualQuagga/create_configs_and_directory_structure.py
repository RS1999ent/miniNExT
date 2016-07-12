import os
import pwd
import grp
import shutil
"""Holds functions related to writing the configuration directory that mininext
will use to start up quagga routers. Currently, bgpd is the only thing being
custom written as the other files are just default files written the same way
for each quagga host.

These methods have no unittest currently because of its interaction with the
file system.

Needs to be ran in sudo mode because permissions on files are changed

"""

daemons_config = """
# This file tells the quagga package which daemons to start.
#
# Entries are in the format: <daemon>=(yes|no|priority)
#   0, "no"  = disabled
#   1, "yes" = highest priority
#   2 .. 10  = lower priorities
# Read /usr/share/doc/quagga/README.Debian for details.
#
# Sample configurations for these daemons can be found in
# /usr/share/doc/quagga/examples/.
#
# ATTENTION: 
#
# When activation a daemon at the first time, a config file, even if it is
# empty, has to be present *and* be owned by the user and group "quagga", else
# the daemon will not be started by /etc/init.d/quagga. The permissions should
# be u=rw,g=r,o=.
# When using "vtysh" such a config file is also needed. It should be owned by
# group "quaggavty" and set to ug=rw,o= though. Check /etc/pam.d/quagga, too.
#
zebra=yes
bgpd=yes
ospfd=no
ospf6d=no
ripd=no
ripngd=no
isisd=no

"""

debian_conf = """
#
# If this option is set the /etc/init.d/quagga script automatically loads
# the config via "vtysh -b" when the servers are started. 
# Check /etc/pam.d/quagga if you intend to use "vtysh"!
#
vtysh_enable=yes
zebra_options=" --daemon -A 127.0.0.1"
bgpd_options="  --daemon -A 127.0.0.1"
ospfd_options=" --daemon -A 127.0.0.1"
ospf6d_options="--daemon -A ::1"
ripd_options="  --daemon -A 127.0.0.1"
ripngd_options="--daemon -A ::1"
isisd_options=" --daemon -A 127.0.0.1"
"""

zebra_conf = """
! Empty config file required to get Zebra to start
"""


def WriteConfigs(host_name_to_bgpdconfig_dict):
    """Function that writes the bgpd configs into the the directory structure of
    the following format:
    config/<host_name>/bgpd.conf
    The directory structure is rooted in the directory that this function in ran in.

    Arguments:
       host_name_to_bgpdconfig_dict: Keyed on the hostname of the host
       and the value is the config to be written.
    """
    #create config directory
    if not os.path.exists('configs'):
        os.makedirs('configs')
    print host_name_to_bgpdconfig_dict
    # for each host, create a subdirectory in config with this host name as the
    # name and write the bgpd config and default config files to it.

    for host_name, bgpdconfig in host_name_to_bgpdconfig_dict.iteritems():
        if not os.path.exists('configs/' + host_name):
            os.makedirs('configs/' + host_name)
        # holds the path to the current host directory we are writing configs
        # to
        path_to_created_directoy = 'configs/' + host_name + '/'
        #write default files
        OpenCreateWrite(path_to_created_directoy + 'daemons', daemons_config)
        OpenCreateWrite(path_to_created_directoy + 'debian.conf', debian_conf )
        OpenCreateWrite(path_to_created_directoy + 'zebra.conf', zebra_conf)
        OpenCreateWrite(path_to_created_directoy + 'bgpd.conf', bgpdconfig)

def DeleteConfigs():
    """deletes the created config directory tree. That is, will recursively delete
    the directory tree rooted by 'configs/'

    If this doesn't exist, nothing should happen
    """
    if os.path.exists('configs'):
        shutil.rmtree('configs')

def OpenCreateWrite(file_path, write_data):
    """ Opens a file (if it doesn't exist, it creates it). Writes data to it and
    closes after write. Makes each file owned by quagga in group quaggavty

    Arguments:
       file_path: name of file as a path from the current directory this function is ran in
       write_data: data to write to the file
    """
    open_file_handle = open(file_path, 'w+')
    open_file_handle.write(write_data)
    open_file_handle.close()

    uid = pwd.getpwnam('quagga').pw_uid
    gid = grp.getgrnam('quaggavty').gr_gid
    os.chown(file_path, uid, gid)

