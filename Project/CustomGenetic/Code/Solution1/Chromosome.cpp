#include <vector>
#include "Graph/Graph.hpp"

#include "Genetic/Solution.hpp"
#include <iostream>
solution solution1
{

class Chromosome
{
public:
    Chromosome(graph::Graph *problem) : problem(problem)
    {
        last_quality = 0;
        changed = true;
        groups.resize(problem->size());
    }

    double fitness()
    {
        if(changed) {
            last_quality = this->_fitness();
            changed = false;
        }
        return last_quality;
    }

    int operator[](int i) const
    {
        return groups[i];
    }

    int &operator[](int i)
    {
        changed = true;
        return groups[i];
    }
    
public:
    int numberOfGroups;

private:
    std::vector<int> groups;
    graph::Graph *problem;

    double last_quality;
    bool changed;


    double _fitness() const
    {
        double quality = 0;
        int m = problem->edgeNumber();
        int problemSize = problem->size();
        for(int i = 0; i < problemSize; ++i) {
            for(int j = 0; j < problemSize; ++j) {
                if(i != j || true) {
                    double weight = (problem->hasEdge(i, j) ? 1 : 0) - (problem->degree(i) * problem->degree(j) / (2.0 * m));
                    quality += weight * (groups[i] == groups[j] ? 1 : 0);
                }
            }
        }
        return quality / (2 * m);
    }
};

};
