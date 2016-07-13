"""
Example service that manages Redis lookup service
"""

from mininext.mount import MountProperties, ObjectPermissions, PathProperties
from mininext.moduledeps import serviceCheck
from mininext.service import Service


class RedisService(Service):

    "Manages Redis lookup service for D-BGP"

    def __init__(self, name="redis-server", **params):
        """Initializes a RedisService instance with a set of global parameters

        Args:
            name (str): Service name (derived class may wish to override)
            params: Arbitrary length list of global properties for this service

        """

        # Verify that Redis is installed"
        serviceCheck('redis-server', moduleName='redis')

        # Call service initialization (will set defaultGlobalParams)
        Service.__init__(self, name=name, **params)

        self.getDefaultGlobalMounts()

    def verifyNodeMeetsServiceRequirements(self, node):
        """Verifies that a specified node is configured to support Redis

        Overrides the :class:`.Service` default verification method to conduct
            checks specific to Ruagga. This includes checking that the node
            has a private log space, a private run space, and is in a PID
            namespace

        Args:
            node: Node to inspect

        """

        if node.inPIDNamespace is False:
            raise Exception("Redis service requires PID namespace (node %s)\n"
                            % (node))

        if node.hasPrivateLogs is False:
            raise Exception("Redis service requires private logs (node %s)\n"
                            % (node))

        if node.hasPrivateRun is False:
            raise Exception("Redis service requires private /run (node %s)\n"
                            % (node))

    def setupNodeForService(self, node):
        """After mounts and other operations taken care of by Service Helper,
           we perform a few last minute tasks here"""

        # Initialize log director'loy
        _, err, ret = node.pexec("mkdir /var/log/redis")
        _, err, ret = node.pexec("chown redis:redis /var/log/redis")

    def getDefaultGlobalParams(self):
        "Returns the default parameters for this service"
        defaults = {'startCmd': '/etc/init.d/redis-server start',
                    'stopCmd': '/etc/init.d/reddis-server stop',
                    'autoStart': True,
                    'autoStop': True,
                    'configPath': None}
        return defaults

    def getDefaultGlobalMounts(self):
        "Service-wide default mounts for the Redis service"

        mounts = []
        mountConfigPairs = {}

        # redis configuration paths
        redisConfigPerms = ObjectPermissions(username='redis',
                                             groupname='redis',
                                              mode=0o775,
                                              strictMode=False,
                                              enforceRecursive=True)
        redisConfigPath = PathProperties(path=None,
                                          perms=redisConfigPerms,
                                          create=True,
                                          createRecursive=True,
                                          setPerms=True,
                                          checkPerms=True)
        redisConfigMount = MountProperties(target='/etc/redis',
                                            source=redisConfigPath)
        mounts.append(redisConfigMount)
        mountConfigPairs['redisConfigPath'] = redisConfigMount

        return mounts, mountConfigPairs
