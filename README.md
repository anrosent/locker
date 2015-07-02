locker: A Lock server
===

This is a simple centralized locking service for distributed applications. It allows clients to create new locks and interact with them via the following API:

 - `client.Lock(server_addr, lock_name)`: Idempotently creates a lock with the given identifier and provides a "reference" to it for the client
 - `Lock.Acquire()`: Blocks the client until it is given the lock
 - `Lock.Release()`: Releases the lock

Not fault-tolerant yet.
