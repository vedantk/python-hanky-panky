#!/usr/bin/python

import sys

for fpath in sys.argv[1:]:
	with open(fpath, 'rb') as f:
		buf = f.read()
		xbuf = (num ^ 8 for num in buf)
		with open(fpath, 'wb') as xout:
			xout.write(bytes(xbuf))

