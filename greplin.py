#!/usr/bin/python

from math import *

gold = (1.0 + sqrt(5)) / 2.0

def longest_palindromic_substring(s):
	cur = ""
	for start in xrange(0, len(s)):
		for end in xrange(start + 1, len(s)):
			orig = s[start:end + 1]
			back = orig[::-1]
			if back == orig and len(orig) > len(cur):
				cur = orig
	return cur

def fibonacci(n):
	fib = (pow(gold, n) - pow(1 - gold, n)) / sqrt(5)
	return int(round(fib))

def is_prime(n):
	up = int(ceil(sqrt(n)))
	if n % 2 == 0 or n % 3 == 0:
		return False
	for it in xrange(6, up + 1, 6):
		if n % (it - 1) == 0 or n % (it + 1) == 0:
			return False
	return True

def next_fib_prime(lower):
	n = floor((log10(lower * sqrt(5)) / log10(gold)) + 0.5)
	while True:
		fib = fibonacci(n)
		if fib > lower and is_prime(fib):
			return fib
		n += 1

def lowest_prime_factor(n):
	for f in xrange(2, int(round(sqrt(n)))):
		if n % f == 0:
			return f
	return 1

def unique_prime_factorization(n):
	factors = []
	while True:
		lpf = lowest_prime_factor(n)
		if lpf == 1:
			factors.append(n if n != 1 else 0)
			return factors
		factors.append(lpf)
		while n % lpf == 0:
			n /= lpf

def powerset(arr):
	if not len(arr):
		return [()]
	else:
		pset = []
		subs = powerset(arr[1:])
		for sub in subs:
			pset.append(sub)
			pset.append((arr[0],) + sub)
		return pset

def nr_subsets_with_dbl_max(arr):
	nr = 0
	pset = powerset(arr)
	for subset in pset:
		if len(subset) <= 1:
			continue
		subset.sort()
		maximum = subset[-1]
		rest = subset[0:-1]
		if sum(rest) == maximum:
			nr += 1

print nr_subsets_with_dbl_max([1, 2, 3, 4, 6])
