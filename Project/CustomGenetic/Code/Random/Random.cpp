#include "Random.hpp"

#include <time.h>

double Random::randomDouble(double min, double max)
{
    std::uniform_real_distribution<double> distribution(min, max);
    return distribution(m_generator);
}

int Random::randomInt(int min, int max)
{
    std::uniform_int_distribution<int> distribution(min, max);
    return distribution(m_generator);
}

std::mt19937 Random::m_generator(time(NULL));
