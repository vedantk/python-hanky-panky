#!/usr/bin/python
# A poor man's k nearest neighbors implementation (vk@vedantk.com).

import math
from collections import namedtuple

# trainer = [(vec: [...], label: object), ...]
TrainingEntry = namedtuple('Entry', ('vec', 'label'))

def dist_euclid(lhs, rhs):
	return math.sqrt(sum(
		[(rhs[k] - lhs[k]) ** 2 for k in range(len(lhs))]
	))

class knn:
	def __init__(self, trainer, dist=dist_euclid, k=3):
		self.k = k
		self.dist = dist
		self.trainer = trainer

	def k_nearest(self, vec):
		pairs = [(elt, self.dist(vec, elt.vec)) for elt in self.trainer]
		pairs.sort(key=lambda pair: pair[1])
		return pairs[:self.k]

	def predict(self, vec):
		'Predict a label for the given vector.'
		labels = {}
		pairs = self.k_nearest(vec)
		for elt in pairs:
			neighbor, val = elt
			votes = labels.get(neighbor.label, 0)
			labels[neighbor.label] = votes + (1 / math.exp(val))
		return max(labels.items(), key=lambda elt: elt[1])[0]

	def regress(self, vec):
		'Given an incomplete input, finds an expected vector.'
		outcome = [0] * len(vec)
		pairs = self.k_nearest(vec)
		for elt in pairs:
			for i in range(len(vec)):
				outcome[i] += elt[0].vec[i]
		return list(map(lambda cell: cell / len(pairs), outcome))
