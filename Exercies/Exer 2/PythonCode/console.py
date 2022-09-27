#from Algorithm.Astar import Astar as search
from Algorithm.UCS import USC as search

from Game.State import Card
from Game.Game import applyMove, printState

def _(x, y):
    return Card(x, y)





s = (
    (_('r', 3), _('r', 2), _('g', 2)),
    (_('b', 1), _('r', 1)),
    (_('g', 3), ),
    (_('b', 3), _('b', 2), _('g', 1))
)

s = (
    (_('r', 4), _('r', 3), _('r', 2), _('g', 2)),
    ( ),
    (_('g', 4), _('b', 1), _('r', 1)),
    (_('g', 3), ),
    (_('b', 4), _('b', 3), _('b', 2), _('g', 1))
)


s = (
    (_('r', 6), _('g', 5), _('r', 5), _('y', 4), ),
    (_('y', 6), _('g', 2), _('r', 4), _('y', 3), _('g', 3), _('y', 2)),
    (_('y', 1), _('g', 4), _('r', 1)),
    (_('g', 6), _('g', 1), _('r', 2), _('y', 5), _('r', 3)),
    ( )
)

print('running A* on ')
printState(s)
moves = search(s, 6)

print()
print(f'solved problem in {len(moves)} moves:')
print(moves)
print('--------')
printState(s)

for move in moves:
    s = applyMove(s, move)
    print(move)
    printState(s)