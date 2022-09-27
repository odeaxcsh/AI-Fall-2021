#if !defined(RANDOM_HPP)
#define RANDOM_HPP

#include <random>

class Random
{
public:
    static int randomInt(int min, int max);
    static double randomDouble(double min, double max);

private:
    static std::mt19937 m_generator;
};

#endif