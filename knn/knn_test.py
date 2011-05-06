import knn

k = knn.knn((
	knn.TrainingEntry((0, 0), 'red'),
	knn.TrainingEntry((5, 5), 'blue'),
))

def test():
	assert k.predict((1, 1)) == 'red'
	assert k.predict((4, 4)) == 'blue'

test()
