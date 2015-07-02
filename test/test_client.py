#!/usr/bin/env python3
import client
import sys
import time
import random
from threading import Thread

''' 
    Test for the Lock Server

    Have a bunch of clients on different threads contend for the lock
    have them add their id to the last element in the data list and 
    append that number.
    Verify at the end that the list is montononically increasing
'''

lockServerAddr = ("localhost", int(sys.argv[1]))
data = [0]

numClients = 10

def testLockClient(n):
    lock = client.Lock(lockServerAddr, 'data')
    lock.Acquire()
    s = data[-1] + n
    data.append(s)
    time.sleep(random.random())
    lock.Release()

threads = []

for i in range(numClients):
    threads.append(Thread(target=testLockClient, args=[random.randint(0,100*numClients)]))

for t in threads:
    t.start()

for t in threads:
    t.join()

assert list(sorted(data)) == data
print("TEST PASSED")
