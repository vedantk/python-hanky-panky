#!/usr/bin/python

import math
from collections import namedtuple

import sys
sys.path.append('..')
import util

# trainer = [TrainingEntry, ...]
TrainingEntry = namedtuple('Entry', ('vec', 'label'))

class knn:
	def __init__(self, trainer=[], dist=util.dist_euclid, k=3):
		self.k = k
		self.dist = dist
		self.trainer = trainer

	def k_nearest(self, vec):
		pairs = [(entry, self.dist(vec, entry.vec))
				for entry in self.trainer]
		pairs.sort(key=lambda pair: pair[1])
		return pairs[:self.k]

	def predict(self, vec):
		'Predict a label for the given vector.'
		labels = {}
		pairs = self.k_nearest(vec)
		for pair in pairs:
			neighbor, dist = pair
			votes = labels.get(neighbor.label, 0)
			labels[neighbor.label] = votes + (1 / math.exp(dist))
		return max(labels.items(), key=lambda elt: elt[1])[0]

	def regress(self, vec):
		'Given an incomplete input, finds an expected vector.'
		outcome = [0.0] * len(vec)
		pairs = self.k_nearest(vec)
		for pair in pairs:
			for i in range(len(vec)):
				outcome[i] += pair[0].vec[i]
		return list(map(lambda cell: cell / len(pairs), outcome))
