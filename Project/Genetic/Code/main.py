from genetic import genetic
from chromosome import connected_components, components_map

from matplotlib import pyplot as plt
import networkx as nx

def getFileName():
    print("Enter the name of the file: ")
    print("or press enter to use the default file: 'sample.txt'")
    fileName = input()
    if fileName == "":
        fileName = "sample.txt"
    return fileName

with open(getFileName(), 'r') as f:
    n = int(f.readline()) # number of vertices
    edges = []
    for line in f:
        a, b = map(int, line.split())
        edges.append((a - 1, b - 1))

G = nx.Graph()
G.add_edges_from(edges)

pos = nx.spring_layout(G)

nx.draw_networkx(G, with_labels=True, pos=pos)

plt.pause(1)

def getProgramParameters():
    generation, population, mutation, crossover = 0, 0, 0, 0
    print("Enter the number of generations: ")
    print("or press enter to use the default value: 100")
    generation = input()
    if generation == "":
        generation = 100
    else:
        generation = int(generation)
    print("Enter the number of chromosomes in the population: ")
    print("or press enter to use the default value: 100")
    population = input()
    if population == "":
        population = 100
    else:
        population = int(population)
    print("Enter the probability of mutation: ")
    print("or press enter to use the default value: 0.1")
    mutation = input()
    if mutation == "":
        mutation = 0.1
    else:
        mutation = float(mutation)
    print("Enter the probability of crossover: ")
    print("or press enter to use the default value: 0.7")
    crossover = input()
    if crossover == "":
        crossover = 0.7
    else:
        crossover = float(crossover)
    return generation, population, mutation, crossover

history = []

for i, (chromosome, fitness) in enumerate(genetic(edges, *getProgramParameters())):
    history.append(fitness)
    tree = components_map(edges, chromosome)
    tree_ = [None] * n
    for j in range(n):
        tree_[j] = tree[j]
    tree = tree_

    print("Generation", i, ":", fitness)

    print()
    print("Chromosome:", chromosome)
    print("Groups:", tree)
    print()
    plt.clf()
    nx.draw(G, cmap=plt.get_cmap('viridis'), node_color=tree, with_labels=True, font_color='white', pos=pos)
    plt.pause(0.1)

print("Final result:", tree)
print("Communities: ", connected_components(edges, chromosome))
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(history)
plt.show()
