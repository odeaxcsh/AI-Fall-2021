#if !defined(PROBLEM_HPP)
#define PROBLEM_HPP

#include <vector>

namespace Move 
{
    typedef struct {
        int from;
        int to;
    } Move;

    using Moves = std::vector<Move>;
};

namespace State
{
    typedef struct {
        int number;
        char color;
    } Card;

    using Section = std::vector<
        Card
    >;

    using State = std::vector<Section>;
    using States = std::vector<State>;

    class Accept{} static accept {}; 
};

namespace GameRules
{
    State::State operator| (const State::State &, const Move::Move &);
    bool operator== (const State::State&, State::Accept); 
    Move::Moves operator* (const State::State &);
};

#endif