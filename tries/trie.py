#!/usr/bin/python

from collections import namedtuple

Terminal = '<EOW>'
Edge = namedtuple('Edge', ('char', 'vtx'))

def search(vtx, s, idx=0):
	'Returns the last vertex and the final search index.'
	if idx == len(s):
		return Terminal, idx
	for edge in vtx:
		if edge.char == s[idx]:
			return search(edge.vtx, s, idx + 1)
	return vtx, idx

def has(vtx, s):
	node, idx = search(vtx, s)
	return node == Terminal

def insert(vtx, s):
	node, idx = search(vtx, s)
	if node == Terminal:
		return
	for k in range(idx, len(s)):
		split = []
		node.append(Edge(s[k], split))
		node = split

def display(vtx, level=0):
	for edge in vtx:
		print("-> " * level + edge.char)
		display(edge.vtx, level + 1)

# brain-dead attempt to compact tries
# I've read a few papers on compact directed acyclic word graphs. It
# doesn't seem too complicated, but I hate sifting through formalism.

def suffixes(s):
	return [s[k:] for k in range(0, len(s) - 3)]

class CompactTrie:
	def __init__(self):
		self.vtx = [] # [edge]
		self.cache = {} # string => vtx

	def insert(self, s):
		node, idx = search(self.vtx, s)
		if node == Terminal:
			return
		for k in range(idx, len(s)):
			suffix = s[k:]
			split = self.cache.get(suffix, [])
			node.append(Edge(s[k], split))
			if len(split):
				return
			else:
				self.cache[suffix] = split
				node = split

def reused(vtx):
	seen = set()
	def visit(node):
		if id(node) in seen:
			print("Re-Use detected!")
			return
		else:
			seen.add(id(node))
		for edge in node:
			visit(edge.vtx)
	visit(vtx)

def test1():
	trie = []
	print(search(trie, 'hello'))
	insert(trie, 'hello')
	display(trie)
	insert(trie, 'hellish')
	display(trie)
	print(search(trie, 'hello'))
	print(search(trie, 'hellish'))
