import re
import knn

def test():
	print("Starting int test.")
	k = knn.knn((
		knn.TrainingEntry((0, 0), 'red'),
		knn.TrainingEntry((5, 5), 'blue'),
	))
	assert k.predict((1, 1)) == 'red'
	assert k.predict((4, 4)) == 'blue'
	for vec in [(0, 0), (2, 4), (5, 5), (7, 9), (-2, -4)]:
		print("Regress[{0}] = {1}".format(vec, k.regress(vec)))

entries = []
entry = re.compile(r"([a-z]+)\s*(\d+)")
with open("../count_big.txt", 'r') as f:
	lines = f.readlines()
	for line in lines:
		entries.append(entry.match(line).groups())

def str_test(nr_train):
	print("Starting str test ({0} sample[s]).".format(nr_train))
	def label(s):
		return "short" if len(word) < 5 else "long"

	k = knn.knn(dist=knn.util.dist_string)
	# k = knn.knn(dist=lambda l, r: abs(len(l) - len(r)))
	for word, count in entries[:nr_train]:
		k.trainer.append(knn.TrainingEntry(word, label(word)))

	errors = 0
	for word, count in entries:
		errors += int(k.predict(word) != label(word))
	print("Error rate: {0}".format(float(errors) / len(entries)))

test()
for n in range(1, 500, 10):
	str_test(n)
