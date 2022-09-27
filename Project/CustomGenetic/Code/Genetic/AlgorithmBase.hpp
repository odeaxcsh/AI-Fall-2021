#if !defined(ALOGRITHM_BASE_HPP)
#define ALOGRITHM_BASE_HPP

#include <vector>
#include "ChromosomeBase.hpp"

namespace genetic {

template <genetic::ChromosomeBase Chromosome>
class AlgorithmBase
{
public:
    virtual Chromosome *crossover(const Chromosome *, const Chromosome *) const = 0;
    virtual Chromosome *mutate(const Chromosome *) const = 0;
    virtual Chromosome *randomChromosome() const = 0;

    virtual ~AlgorithmBase() { }
};

}

#endif