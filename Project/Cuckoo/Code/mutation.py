import numpy as np

def mutation(m, X):
    newHabitat = np.copy(X)
    n = np.random.randint(0, m)
    indices = np.random.randint(0, m, n)
    newHabitat[indices] = np.bitwise_xor(X[indices], 1)
    return newHabitat
