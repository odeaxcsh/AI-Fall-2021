from typing import List, Tuple
from .Move import Move, Moves
from .State import State, Section, Card
from copy import deepcopy
from itertools import product

from Core.Utilities import toList, toTuple, star

def applyMove(state: State, move: Move) -> State:
    if not len(state[move.o]):
        raise Exception(f'There is nothing to move from {move.o}')

    if move.o == move.d:
        raise Exception('Cannot move a card form a section to itself')

    if len(state[move.d]) and state[move.d][-1].number < state[move.o][-1].number:
        raise Exception(f'Cannot move a card with value of {state[move.o][-1]} opon of a card with value of {state[move.d][-1]}')
    
    newState = toList(state)
    newState[move.d].append(
        newState[move.o].pop()
    )
    return toTuple(newState)


def getAllMoves(sections: List[Section]) -> Moves:
    n = len(sections)
    '''bunch of connected pipes
    i in 1..n =(filter if ith section is not empty)|
                                                   |=> (i, j) =(filter if move (i, j) breaks games rules)=> convert (i, j) to a Move object 
                                      j in 1..n    |
    '''
    return map(
        star(lambda x, y: Move(x, y)),
        filter(
            star(lambda i, j: (i != j) and (not sections[j] or sections[i][-1].number <= sections[j][-1].number)),
            product(
                filter(
                    lambda i: len(sections[i]),
                    range(n)
                ),
                range(n)
            )
        )
    )

def isAccept(state: State, m):
    '''
        check if all of section pass following conditons
            cards numbers are correspond to 1..m
            all card have same color
    '''
    return all(
        len(section) == 0 or len(section) == m and all(
            i == card.number for i, card in enumerate(reversed(section), 1)
        ) and all(
            section[0].color == card.color for card in section
        ) for section in state
    )


def printState(state: State):
    for section in state:
        if not len(section):
            print('#')
        else:
            print(' '.join(map(str, section)))
    print()