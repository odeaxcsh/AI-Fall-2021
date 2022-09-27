from Game.Game import applyMove, isAccept, getAllMoves
from .DS.FibonacciHeap import Fibonacci_Heap

from math import inf

def _extractMoves(parents, finalState):
    state = finalState
    path = []
    while parents[state] is not None:
        state, move = parents[state]
        path.append(move)
    return list(reversed(path))

def _pushToHeap(hcost, gcost, depth, state, heap):
    return heap.add(hcost + gcost, (gcost, depth, state))


def _popFromHeap(heap):
    gh, (g, depth, state) = heap.remove_min()
    return gh - g, g, depth, state

def BaseSearchAlgorithm(initialState, h, g, m):
    heap = Fibonacci_Heap() # (g + h as key, (g, state, depth) as value)
    parent, toExpand, cloud = {}, {}, set()
    allexpandedCount = 0

    # log helper variables
    currentCostLevel = -inf
    maxDepthOfCurrentCostLevel = -inf
    minDepthOfCurrentCostLevel = inf
    currentCostLevelNodesCount = 1
    currenCostLevelChildrens = 0
    seenNodesFromLastLog = 0

    def _log():
        print(f'cost level {currentCostLevel} exceeded')
        print(f'\t number of nodes on this level: {currentCostLevelNodesCount} from depth of {minDepthOfCurrentCostLevel} to {maxDepthOfCurrentCostLevel}')
        print(f'\t new children nodes added: {currenCostLevelChildrens}')
        # print(f'\t net increase of nodes: {currenCostLevelChildrens - currentCostLevelNodesCount}')
        print(f'\t branching factor: {currenCostLevelChildrens/currentCostLevelNodesCount}')
        #print(f'\t deep most node: \n\t\t' + '\n\t\t'.join(str(section) for section in deepMostNode))
        print()

    finalState = None
    parent[initialState] = None
    toExpand[initialState] = _pushToHeap(0, g(initialState, m), 0, initialState, heap)

    while finalState is None:
        if heap.empty():
            raise Exception('Problem is not solvable\n search all of possinble solutions and found no answer')
        
        cost, gcost, depth, state = _popFromHeap(heap)

        cloud.add(state)
        seenNodesFromLastLog += 1
        allexpandedCount += 1

        # log search information
        # if seenNodesFromLastLog > 5000:
        #     _log()
        #     seenNodesFromLastLog = 0
        
        if cost + gcost - currentCostLevel > 0:
            if currentCostLevel != -inf:
                _log()
                seenNodesFromLastLog = 0
            currentCostLevel = cost + gcost
            maxDepthOfCurrentCostLevel = -inf
            minDepthOfCurrentCostLevel = inf
            currentCostLevelNodesCount = 0
            currenCostLevelChildrens = 0
        
        currentCostLevelNodesCount += 1
        minDepthOfCurrentCostLevel = min(minDepthOfCurrentCostLevel, depth)
        if maxDepthOfCurrentCostLevel < depth:
            maxDepthOfCurrentCostLevel = depth

        if isAccept(state, m):
            finalState = state
        
        for move in getAllMoves(state):
            childState = applyMove(state, move)
            
            if childState in cloud:
                continue
            
            currenCostLevelChildrens += 1

            if childState not in toExpand:
                parent[childState] = (state, move)
                toExpand[childState] = _pushToHeap(cost + h(state, move, childState), g(childState, m), depth + 1, childState, heap)
            else:
                heap.decrease(toExpand[childState], cost + h(state, move, childState) + toExpand[childState].location.value[0])
    _log()
    print(f'total number of expanded nodes: {allexpandedCount}')
    return _extractMoves(parent, finalState)
