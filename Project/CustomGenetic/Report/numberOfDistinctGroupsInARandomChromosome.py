import numpy as np
import matplotlib.pyplot as plt

def randomChromosome(n):
    return np.random.randint(0, n, n)

def numberOfDistinctGroupsOf(chromosome):
    return len(set(chromosome))

def averageNumberOfDistinctGroupsOver(n, numberOfTests):
    return sum(numberOfDistinctGroupsOf(randomChromosome(n)) for _ in range(numberOfTests)) / numberOfTests


x = np.arange(1, 1000, 10)
y = np.array([averageNumberOfDistinctGroupsOver(i, 1000) for i in x])

plt.plot(x, y, label="distinct groups per graph size")
plt.plot(x, 0.6 * x, label="6/10 x")
plt.legend()
plt.show()