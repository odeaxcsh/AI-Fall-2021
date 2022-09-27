
import numpy as np

def crossover(m, X, Y):
    return np.random.randint(0, 2, m) * (X - Y) + Y
