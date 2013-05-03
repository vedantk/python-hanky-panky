import math

def factorial(n):
	return int(math.gamma(n + 1))

def C(n, k):
	return factorial(n) / (factorial(k) * factorial(n - k))

if __name__ == '__main__':
	for n in range(100, 1000):
		for k in range(n, n + 10):
			C(n, k)
