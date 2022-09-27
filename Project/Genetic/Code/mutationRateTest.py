import numpy as np
from matplotlib import pyplot as plt

from genetic import genetic

with open('sample.txt', 'r') as f:
    n = int(f.readline()) # number of vertices
    edges = []
    for line in f:
        a, b = map(int, line.split())
        edges.append((a - 1, b - 1))


n = 30
mutationRates = np.linspace(0.1, 0.9, n)
crossoverRates = np.repeat(0.5, n)

generations = 30
populationSize = 30

history = np.zeros((n, generations))

for mutationRate, crossoverRate, i, in zip(mutationRates, crossoverRates, range(n)):
    print("running with mutationRate: " + str(mutationRate) + " and crossoverRate: " + str(crossoverRate))
    
    history[i, :] = np.array([
        ret[1] for ret in genetic(edges, populationSize, generations, mutationRate, crossoverRate)
    ])

    # print the best fitness
    print(history[i, :].max())
    print()

for i in range(n):
    plt.plot(history[i, :], label=str(mutationRates[i]))
plt.legend()
plt.show()