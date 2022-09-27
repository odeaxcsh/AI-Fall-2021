#include "Core/GameCore/Problem.hpp"
#include "Core/Libs/Utils.hpp"

#include <stdexcept>

namespace Internal {
    bool allHaveSameColor(const State::Section &section)
    {
        if(section.empty()) {
            return true;
        }
    
        char fisrtCardColor = section[0].color;
        return Aggregate::all(
            section,
            [fisrtCardColor](const State::Card &card) -> bool {
                return card.color == fisrtCardColor;
            }
        );
    }

    bool areSorted(const State::Section &section)
    {
        int prev = 0;
        return Aggregate::all(
            section,
            [&prev](const State::Card &card) -> bool {
                bool result = (card.number >= prev);
                prev = card.number;
                return result;
            }
        );
    }
};

bool GameRules::operator==(const State::State &state, State::Accept)
{
    return Aggregate::all(
        state,
        [](const State::Section &section) -> bool {
            return Internal::allHaveSameColor(section) and Internal::allHaveSameColor(section);
        }
    );
}

Move::Moves GameRules::operator*(const State::State &state)
{
    int n = state.size();
    return Iterate::apply<std::pair<int, int>, Move::Move> (
        Aggregate::filter(
            Iterate::product(
                Aggregate::filter(
                    Generate::range(n),
                    [&state](int i){ return not state[i].empty(); }
                ),
                Generate::range(n)
            ),
            [&state](const std::pair<int, int> &move){
                return state[move.second].empty() or state[move.first].back().number <= state[move.second].back().number;
            }
        ),
        [](const std::pair<int, int> &move) -> Move::Move {
            return Move::Move {
                .from = move.first,
                .to = move.second
            };
        }
    );
}

State::State GameRules::operator|(const State::State &state, const Move::Move &move)
{
    State::State nextState = state;
    if(state[move.from].empty()) {
        throw std::runtime_error("origin list is empty.");
    }

    if(not state[move.to].empty() and state[move.from].back().number > state[move.to].back().number) {
        throw std::runtime_error("trying to break game rules.");
    }

    nextState[move.from].pop_back();
    nextState[move.to].push_back(state[move.from].back());
    return nextState;
}