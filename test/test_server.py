#!/usr/bin/env python3
import server
import sys

locksrv = server.LockServer(("localhost", int(sys.argv[1])))

