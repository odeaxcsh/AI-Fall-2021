#include "Random/Random.hpp"
#include "Chromosome.cpp"
#include "Genetic/AlgorithmBase.hpp"
#include "Genetic/Solution.hpp"

#include <algorithm>
#include <random>
#include <cmath>
#include <climits>

#include <iostream>

solution solution1
{
class Algorithm : public genetic::AlgorithmBase<Chromosome>
{
public:
    Algorithm(graph::Graph *problem) : problem(problem) 
    {
    }

    virtual Chromosome *randomChromosome() const override
    {
        Chromosome *chromosome = new Chromosome(problem);
        int problemSize = problem->size();
        chromosome->numberOfGroups = problemSize;
        for(int i = 0; i < problemSize; ++i) {
            (*chromosome)[i] = Random::randomInt(0, problemSize - 1);
        }

        this->_normalize(chromosome);
        return chromosome;
    }

    virtual Chromosome *mutate(const Chromosome *chromosome) const override
    {
        auto freq = _getGroupFrequency(chromosome);
        auto totalReciprocalSum = std::accumulate(freq.begin(), freq.end(), 0.0, [](double sum, double x) { return sum + 1.0 / x; });
        auto r = Random::randomDouble(0.0, totalReciprocalSum);
        int group = 0;
        double sum = 0.0;
        for(std::size_t i = 0; i < freq.size(); ++i) {
            sum += 1.0 / freq[i];
            if(sum >= r) {
                group = i;
                break;
            }
        }

        Chromosome *newChromosome = new Chromosome(*chromosome);
        int problemSize = problem->size();
        for(int i = 0; i < problemSize; ++i) {
            if((*newChromosome)[i] == group) {
                auto adjacent = problem->getAdj(i);
                if(adjacent.size() > 0) {
                    int n = Random::randomInt(0, adjacent.size() - 1);
                    auto begin = adjacent.begin();
                    std::advance(begin, n);
                    (*newChromosome)[i] = (*newChromosome)[*begin];
                } else {
                    (*newChromosome)[i] = 0;
                }
            } else {
                (*newChromosome)[i] = (*newChromosome)[i];
            }
        }
        this->_normalize(newChromosome);
        return newChromosome;
    }

    virtual Chromosome *crossover(const Chromosome *chromosome1, const Chromosome *chromosome2) const override
    {
        Chromosome *newChromosome = new Chromosome(problem);
        int problemSize = problem->size();
        newChromosome->numberOfGroups = std::max(chromosome1->numberOfGroups, chromosome2->numberOfGroups);
        for(int i = 0; i < problemSize; ++i) {
            if(Random::randomInt(0, 1)) {
                (*newChromosome)[i] = (*chromosome1)[i];
            } else {
                (*newChromosome)[i] = (*chromosome2)[i];
            }
        }

        this->_normalize(newChromosome);
        return newChromosome;
    }

public:
    graph::Graph *problem;

private:
    std::vector<int> _getGroupFrequency(const Chromosome *chromosome) const
    {
        std::vector<int> groupFrequency(chromosome->numberOfGroups, 0);
        int problemSize = problem->size();
        for(int i = 0; i < problemSize; ++i) {
            ++groupFrequency[(*chromosome)[i]];
        }
        return groupFrequency;
    }

    void _normalize(Chromosome *chromosome) const
    {   
        std::vector<int> groupMapping(problem->size(), INT_MAX);
        int lastUsedGroup = 0;
        for(int i = 0; i < problem->size(); ++i) {
            if(groupMapping[(*chromosome)[i]] == INT_MAX) {
                groupMapping[(*chromosome)[i]] = lastUsedGroup;
                ++lastUsedGroup;
            }
        }

        for(int i = 0; i < problem->size(); ++i) {
            (*chromosome)[i] = groupMapping[(*chromosome)[i]];
        }

        int numberOfGroups = 0;
        for(int i = 0; i < problem->size(); ++i) {
            if(numberOfGroups < (*chromosome)[i]) {
                numberOfGroups = (*chromosome)[i];
            }
        }
        chromosome->numberOfGroups = numberOfGroups + 1;
    }
};

}

