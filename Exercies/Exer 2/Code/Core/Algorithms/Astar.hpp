#ifndef ASTAR_HPP
#define ASTAR_HPP

#include "Core/GameCore/Problem.hpp"
#include "Core/Libs/Heap.hpp"

#include <utility>
#include <functional>
#include <vector>
#include <unordered_map>
#include <algorithm>

std::pair<Move::Moves, State::State> aStar(const State::State &initialState, std::function<int(const State::State &)> h)
{
    
}

#endif
