import thinrpc

class Lock(object):

    def __init__(self, addr, lock_name):
        self.server = thinrpc.RpcRemote(addr, timeout=e)
        self.name = lock_name
        res = self.server.CreateLock(lock_name)
        if not res.ok:
            raise ValueError(res.msg)

    def Lock(self):
        self.server.Lock(self.name)

    def Release(self):
        self.server.Release(self.name)
