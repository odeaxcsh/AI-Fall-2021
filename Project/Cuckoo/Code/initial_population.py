import numpy as np

def initial_population(m, size):
    return np.random.randint(0, 2, (size, m))


