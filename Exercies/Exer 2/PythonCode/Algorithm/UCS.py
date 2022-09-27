from .BaseSearchAlgorithm import BaseSearchAlgorithm

def USC(initialState, m):
    def costFunction(parent, move, cost):
        return 1
    
    def heuristicFunction(state, m):
        return 0
    
    return BaseSearchAlgorithm(initialState, costFunction, heuristicFunction, m)
