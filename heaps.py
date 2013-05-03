#!/usr/bin/python

import math
import itertools

class MaxHeap:
	def __init__(self):
		self.heap = []

	def _lchildOf(self, idx):
		return (2 * idx) + 1

	def _rchildOf(self, idx):
		return (2 * idx) + 2

	def _parentOf(self, idx):
		return int((idx - 1) / 2)

	def insert(self, elt):
		self.heap.append(elt)
		self._percolateUp(len(self.heap) - 1)

	def _percolateUp(self, idx):
		parent = self._parentOf(idx)
		if self.heap[idx] > self.heap[parent]:
			self.heap[idx], self.heap[parent] = (
				self.heap[parent], self.heap[idx]
			)
			self._percolateUp(parent)

	def print(self):
		print("*" * 50)
		self._display([0], int(math.log(len(self.heap) + 1, 2)))
		print("self.heap =", self.heap)

	def _display(self, idxs, lvl):
		visit = list(filter(lambda idx: idx < len(self.heap), idxs))
		if not len(visit):
			return
		print('  ' * lvl, '  '.join([str(self.heap[elt]) for elt in visit]))
		visit = itertools.chain(map(self._lchildOf, visit),
					map(self._rchildOf, visit))
		self._display(visit, lvl - 1)

if __name__ == '__main__':
	mh = MaxHeap()
	mh.print()
	mh.insert(1)
	mh.print()
	import random
	for i in range(10):
		mh.insert(random.randint(1, 10))
		mh.print()
