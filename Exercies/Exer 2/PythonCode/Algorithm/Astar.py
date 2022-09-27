from .BaseSearchAlgorithm import BaseSearchAlgorithm

def Astar(initialState, m):
    def colorsHeuristicFunction(state, m):
        return sum(
            sum(
                (card.color != section[0].color) * (len(section) - i) for i, card in enumerate(section)
            ) for section in state
        )
    
    def misplacedHeuristicFunction(state, m):
        return sum(
            sum(
                (section[i].number != m - i) * (m - i) if i < len(section) else (1) for section in state
            ) for i in range(m)
        )

    def heuristicFunction(state, m):
        return (misplacedHeuristicFunction(state, m) + colorsHeuristicFunction(state, m))

    def costFunction(parent, move, cost):
        return 1

    return BaseSearchAlgorithm(initialState, costFunction, heuristicFunction, m)

