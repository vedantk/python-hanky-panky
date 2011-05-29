import math
from collections import namedtuple 

class Obj:
	def __init__(self, **kwargs):
		for key, val in kwargs.items():
			setattr(self, key, val)

class memoized:
	def __init__(self, func):
		self.func = func
		self.cache = {}

	def __call__(self, *args):
		try:
			return self.cache[args]
		except KeyError:
			value = self.func(*args)
			self.cache[args] = value
			return value
		except TypeError:
			return self.func(*args)

class MultiKeyDict(dict):
	def __setitem__(self, vec, val):
		if type(vec) in (list, tuple): 
			for key in vec:
				super().__setitem__(self, key, val)
		else:
			super().__setitem__(self, vec, val)

@memoized
def dist_euclid(lhs, rhs):
        return math.sqrt(math.fsum(
                [(rhs[k] - lhs[k]) ** 2 for k in range(len(lhs))]
        ))

@memoized
def dist_string(target, source, cutoff=None):
        n, m = len(target), len(source)
        distance = [[0 for i in range(m + 1)] for j in range(n + 1)]
        for i in range(1, n + 1):
                distance[i][0] = distance[i-1][0] + 1
        for j in range(1, m + 1):
                distance[0][j] = distance[0][j-1] + 1
        for i in range(1, n + 1):
                for j in range(1, m + 1):
                        distance[i][j] = min(distance[i-1][j] + 1,
                                                distance[i][j-1] + 1,
                                                distance[i-1][j-1] + \
                                                int(source[j-1] != target[i-1]))
                        if cutoff != None and distance[i][j] > cutoff:
                                return False
        return True if cutoff != None else distance[n][m]

