#if !defined(GENETIC_ALGORITHM_HPP)
#define GENETIC_ALGORITHM_HPP

#include "Random/Random.hpp"

#include "ChromosomeBase.hpp"
#include "AlgorithmBase.hpp"

#include <vector>
#include <memory>
#include <iostream>
namespace genetic {

template <genetic::ChromosomeBase Chromosome>
class GeneticAlgorithm
{
public:
    GeneticAlgorithm(AlgorithmBase<Chromosome> *algorithm, 
        double crossoverRate, double mutationRate, int maxGenerations, int populationSize
    ) 
        : m_population(populationSize), 
        m_algorithm(algorithm), 
        m_crossoverRate(crossoverRate), 
        m_mutationRate(mutationRate), 
        m_maxGenerations(maxGenerations), 
        m_populationSize(populationSize)
    {
        for(int i = 0; i < m_populationSize; i++) {
            m_population[i] = m_algorithm->randomChromosome();
        }   
    }

    GeneticAlgorithm &nextGeneration()
    {
        ++this->m_currentGeneration;

        std::vector<Chromosome *> newPopulation;
        for(int i = 0; i < m_populationSize; ++i) {
            if(Random::randomDouble(0.0, 1.0) < m_crossoverRate) {
                Chromosome *parent1 = selectParent();
                Chromosome *parent2 = selectParent();
                Chromosome *child = m_algorithm->crossover(parent1, parent2);
                newPopulation.push_back(child);
            }
        }

        this->m_population.insert(m_population.end(), newPopulation.begin(), newPopulation.end());

        for(int i = 0; i < m_populationSize; ++i) {
            if(Random::randomDouble(0.0, 1.0) < m_mutationRate) {
                m_population.push_back(m_algorithm->mutate(m_population[i]));
            }
        }

        // sort population by fitness and number of groups
        std::sort(m_population.begin(), m_population.end(), [](Chromosome *a, Chromosome *b) {
            return a->fitness() > b->fitness() or (a->fitness() == b->fitness() and a->numberOfGroups < b->numberOfGroups);
        });

        std::for_each(m_population.begin() + m_populationSize, m_population.end(), [](Chromosome *c) {
            delete c;
        });
        m_population.erase(m_population.begin() + m_populationSize, m_population.end());
        return *this;
    }

    bool finished() const
    {
        return m_currentGeneration >= m_maxGenerations;
    }

    Chromosome *selectParent() const
    {
        double totalFitness = 0;
        for(auto ptr : m_population) {
            totalFitness += ptr->fitness();
        }

        double random = Random::randomDouble(0.0, totalFitness);
        double current = 0;
        for(auto ptr : m_population) {
            current += ptr->fitness();
            if(current >= random) {
                return ptr;
            }
        }

        return m_population[0];
    }

    Chromosome *bestFit() const
    {
        Chromosome *best = m_population[0];
        double bestFitness = best->fitness();
        for(int i = 1; i < m_populationSize; ++i) {
            double thisFitt = m_population[i]->fitness();
            if(thisFitt > bestFitness) {
                best = m_population[i];
                bestFitness = thisFitt;
            }
        }
        return best;
    }

    ~GeneticAlgorithm()
    {
        for(int i = 0; i < m_populationSize; ++i) {
            delete m_population[i];
        }
    }

protected:
    std::vector<Chromosome *> m_population;
    AlgorithmBase<Chromosome> *m_algorithm;
    double m_crossoverRate;
    double m_mutationRate;
    int m_maxGenerations;
    int m_populationSize;
    int m_currentGeneration = 0;
};

};

#endif