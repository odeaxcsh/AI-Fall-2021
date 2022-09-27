#if !defined(CHROMOSOME_BASE_HPP)
#define CHROMOSOME_BASE_HPP

#include <concepts>

namespace genetic 
{

template <typename T>
concept ChromosomeBase = requires(T chrmosome)
{
    { chrmosome.fitness() } -> std::convertible_to<double>;
};

}

#endif