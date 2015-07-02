import logging
from thinrpc import RpcApplication, RpcModule, RpcMessage, logger, OK
import threading

logger.setLevel(logging.DEBUG)

# TODO: release lock on connection break... would need more stateful connection

class LockServer(RpcApplication):
    
    def __init__(self, addr):
        self.addr = addr
        self.locks = {}
        self.owners = {}
        self.ctr = 0

        self.Start(single_threaded=False)

    def _get_id(self):
        i = self.ctr
        self.ctr += 1
        return i

    @RpcModule.Method
    def Lock(self, sender, lock_name):
        if lock_name not in self.locks:
            return "lock %s does not exist" % lock_name, None

        logger.debug("%s wants the lock", sender, extra={"mode":"server"})
        client_id = self._get_id()
        self.locks[lock_name].acquire()
        self.owners[lock_name] = client_id
        logger.debug("%s has the lock w/ id %s", sender, client_id, extra={"mode":"server"})
        return OK, client_id

    @RpcModule.Method
    def Release(self, sender, lock_name, client_id):
        if lock_name not in self.locks:
            return "lock %s does not exist" % lock_name, None

        if client_id != self.owners[lock_name]:
            return "you do not own lock %s" % lock_name, None

        self.owners[lock_name] = None
        self.locks[lock_name].release()
        logger.debug("%s has released lock" % sender, extra={"mode":"server"})
        return OK, None

    @RpcModule.Method
    def CreateLock(self, sender, lock_name):

        logger.debug("creating lock %s", lock_name, extra={"mode":"server"})

        # Create is idempotent, so don't error
        if lock_name in self.locks:
            return OK, None

        self.locks[lock_name] = threading.Lock()
        self.owners[lock_name] = None
        return OK, None

