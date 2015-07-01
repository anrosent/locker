import thinrpc
import threading

class LockServer(thinrpc.RpcApplication):
    
    def __init__(self, addr):
        self.addr = addr
        self.locks = {}
        self.owners = {}

        self.Start()

    @RpcModule.Method
    def Lock(self, client, lock_name):
        if lock_name not in self.locks:
            return RpcMessage(ok=False, msg="lock %s does not exist" % lock_name)

        self.locks[lock_name].acquire()
        self.owners[lock_name] = client
        return RpcMessage(ok=True)

    @RpcModule.Method
    def Unlock(self, client, lock_name):
        if lock_name not in self.locks:
            return RpcMessage(ok=False, msg="lock %s does not exist" % lock_name)

        if client != self.owners[lock_name]:
            return RpcMessage(ok=False, msg="you do not own lock %s" % lock_name)

        self.owners[lock_name] = None
        self.locks[lock_name].release()
        return RpcMessage(ok=True)

    @RpcModule.Method
    def CreateLock(self, client, lock_name):
        if lock_name in self.locks:
            return RpcMessage(ok=False, msg='lock %s exists' % lock_name)

        self.locks[lock_name] = threading.Lock()
        self.owners[lock_name] = None
        return RpcMessage(ok=True)

