import numpy as np
from mutation import mutation   
from crossover import crossover
from initial_population import initial_population
from chromosome import fitness

def genetic(
        allEdges,
        populationSize,
        maxGenerations,
        mutationProbability,
        crossoverProbability
    ):
    m = len(allEdges)
    population = initial_population(m, populationSize)
    for generation in range(maxGenerations):
        if np.random.random() < crossoverProbability:
            for i in range(populationSize):
                j = np.random.randint(0, populationSize)
                population = np.vstack((population, crossover(m, population[i], population[j])))
        
            for i in range(len(population)):
                if np.random.random() < mutationProbability:
                    population = np.vstack((population, mutation(m, population[i])))
        
        population = sorted(population, key=lambda c: fitness(allEdges, c), reverse=True)
        population = population[:populationSize]
        yield population[0], fitness(allEdges, population[0])
    return population[0], fitness(allEdges, population[0])
