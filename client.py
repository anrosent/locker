import logging
import thinrpc

thinrpc.logger.setLevel(logging.DEBUG)

class Lock(object):

    def __init__(self, addr, lock_name):
        self.server = thinrpc.RpcRemote(addr, timeout=None)
        self.name = lock_name
        self.client_id = None
        res = self.server.CreateLock(lock_name=lock_name)
        if res.err:
            raise ValueError(res.err)

    def Lock(self):
        res = self.server.Lock(lock_name=self.name)
        if res.err:
            raise ValueError(res.err)
        self.client_id = res.result

    def Release(self):
        if self.client_id is None:
            raise ValueError("Cannot release a lock you don't hold")

        self.server.Release(lock_name=self.name, client_id=self.client_id)

