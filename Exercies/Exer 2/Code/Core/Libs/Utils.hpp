#if !defined(UTILS_HPP)
#define UTILS_HPP

#include <vector>
#include <numeric>
#include <functional>

namespace Aggregate 
{
    template <typename dtype, typename lambda>
    bool all(const std::vector<dtype> &data, lambda condition)
    {
        for(const dtype &d : data) {
            if(not condition(d)) {
                return false;
            }
        }
        return true;
    }

    template <typename dtype, typename lambda>
    bool any(const std::vector<dtype> &data, lambda condition)
    {
        for(const dtype &d : data) {
            if(condition(d)) {
                return true;
            }
        }
        return false;
    }

    template <typename dtype, typename lambda>
    std::vector<dtype> filter(const std::vector<dtype> &data, lambda condition)
    {
        std::vector<dtype> result;
        for(const dtype &d : data) {
            if(condition(d)) {
                result.push_back(d);
            }
        }
        return result;
    }
};

namespace Iterate 
{
    template <typename dtype, typename etype>
    std::vector<std::pair<dtype, etype>> product(const std::vector<dtype> &data, const std::vector<etype> &eata)
    {
        std::vector<std::pair<dtype, etype>> result; 
        for(const dtype &d : data) {
            for(const etype &e : eata) {
                result.push_back(std::make_pair(d, e));
            }
        }
        return result;
    }

    template <typename dtype, typename otype>
    std::vector<otype> apply(const std::vector<dtype> &data, std::function<otype(const dtype &)> f)
    {
        std::vector<otype> result;
        for(const dtype &d : data) {
            result.push_back(f(d));
        }
        return result;
    }

    template <typename dtype, typename lambda>
    void foreach(const std::vector<dtype> &data, lambda fn) 
    {
        for(const dtype &d : data) {
            fn(d);
        }
    }
}

namespace Generate
{
    std::vector<int> range(int n, int m = -1) 
    {
        if(m == -1) {
            m = n - 1;
            n = 0;
        }
        std::vector<int> result(m - n + 1);
        std::iota(result.begin(), result.end(), n);
        return result;
    }
}

#endif