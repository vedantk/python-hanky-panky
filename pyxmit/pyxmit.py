#!/usr/bin/python
# pyxmit - send Python jobs to other computers!

'''
To send a job, place all of the relevant Python code in a single file.
Define the following functions in the module:

	def onPeerRecv():
		# Called when another computer receives your code. Whatever
		# object this function returns will be sent back to your server.

	def onJobReturn(result):
		# Called when you receive the result for your job.

Finally, run pyxmit and call 'dispatch(host, fname)' (where host is any
IPv4 address and fname is the relative path to your script).

Warning / Peligro / Advertencia / Danger:
	Any pyxmit instance may process untrusted, unauthenticated, and
	arbitrary Python code while leaving behind little forensic evidence.
	Don't run it on an open port. Really, that doesn't need to be said.
'''

import io
import code
import socket
import pickletools
import pickle
import zlib
from threading import Thread
from socketserver import StreamRequestHandler, TCPServer, ThreadingMixIn

PORT = 5403
JOBS = {} # JobID : (DB_MOD, DB_REQ)
REQ_TYPE = 0
REQ_JobID = 1
REQ_OBJ = 2
DB_MOD = 0
DB_REQ = 1
xmitJob = hash('xmitJOB')
xmitReply = hash('xmitREPLY')

def serialize(pyobj):
	sbuf = io.StringIO()
	pickle.dump(pyobj, sbuf, pickle.HIGHEST_PROTOCOL)
	return zlib.compress(pickletools.optimize(sbuf.getvalue()))

def sendTo(host, data):
	sock = socket.socket()
	sock.connect((host, PORT))
	sock.send(data)
	sock.close()

def notice(msg):
	print('\n[Message]')
	print(msg)
	print('[\\Message]')

class Server(TCPServer, ThreadingMixIn):
	allow_reuse_address = True

class Handler(StreamRequestHandler):
	def handle(self):
		msg = self.rfile.read()
		tup = pickle.loads(zlib.decompress(msg))

		if tup[REQ_TYPE] == xmitJob:
			notice('Someone sent you a job (ID=%d).' % tup[REQ_JobID])
			reply = serialize((xmitReply, tup[REQ_JobID], procJob(tup)))
			sendTo(self.client_address[0], reply)
		elif tup[REQ_TYPE] == xmitReply:
			notice('Someone did a job (ID=%d) for you.' % tup[1])
			mod = JOBS[tup[REQ_JobID]][DB_MOD]
			mod.onJobReturn(tup[REQ_OBJ])

def procJob(tup):
	fname = str(tup[REQ_JobID])
	with open(fname + '.py', 'w') as f:
		f.write(tup[REQ_OBJ])
	mod = __import__(fname)
	return mod.onPeerRecv()

def dispatch(host, fname):
	text = open(fname, 'r').read()
	jobID = hash(text)
	if jobID not in JOBS:
		if fname.endswith('.py'):
			fname = fname[:fname.rfind('.')]
		mod = __import__(fname)
		if 'onPeerRecv' and 'onJobReturn' not in dir(mod):
			return notice("%s lacks either 'onPeerRecv' or 'onJobReturn'.")
		req = serialize((xmitJob, jobID, text))
		JOBS[jobID] = (mod, req)
	else:
		req = JOBS[jobID][DB_REQ]
	sendTo(host, req)
	notice('Your job (ID=%d) was sent to %s.' % (jobID, host))

def serve(*args):
	global xmit
	xmit = Server(('localhost', PORT), Handler)
	xmit.serve_forever()

def quit():
	xmit.shutdown()
	print()
	exit()

def xm_input(prompt):
	try:
		s = input(prompt)
	except EOFError:
		quit()
	return s

def repl(*args):
	code.interact(':: pyxmit Shell\t[quit() or Ctl-D to exit.]', xm_input, {
		'dispatch' : dispatch,
		'test' : lambda: dispatch('localhost', 'test-xmit.py'),
		'quit' : quit
	})

if __name__ == '__main__':
	print("Loading...")
	serv = Thread(target=serve)
	shell = Thread(target=repl)
	serv.start()
	shell.start()
