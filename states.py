import numpy as np


def diagonals(size=100):
	"""Above and below diagonals."""

	if isinstance(size, int):
		size = (size,)*2

	state = np.zeros(size, dtype=np.int8)
	for i in range(1, state.shape[1]-1):
		state[i-1, i] = state[i+1, i] = state[i, -i-2] = state[i, -i] = 1

	state[1, 0] = state[0, -2] = state[-1, 1] = state[-2, -1] = 1
	return state


def random(size=100):
	"""Randomly generated state."""

	if isinstance(size, int):
		size = (size,)*2

	return np.random.randint(0, 2, size[0]*size[1], dtype=np.int8).reshape(size)


def empty(size=100):
	"""An empty state."""

	if isinstance(size, int):
		size = (size,)*2

	return np.zeros(size, dtype=np.int8)

