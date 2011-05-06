# test-xmit.py

import time

def factorial(n):
	if n <= 1: return 1
	return n * factorial(n - 1)

def onPeerRecv():
	beg = time.time()
	nr = factorial(250)
	return (nr, time.time() - beg)

def onJobReturn(result):
	print "factorial(250) = %d. Time = %f secs." % (result[0], result[1])
