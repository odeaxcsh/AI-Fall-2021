import numpy as np

def construct_tree(edges, mask=None):
    # type: (np.ndarray, list) -> dict
    n = len(set(v[0] for v in edges).union(v[1] for v in edges))

    vertices = {i: [] for i in range(n)}
    for i, v in enumerate(edges):
        if mask is None or mask[i]:
            vertices[v[0]].append(v[1])
            vertices[v[1]].append(v[0])
    return vertices


def connected_components(edges, mask=None):
    # type: (np.ndarray, list) -> list
    tree = construct_tree(edges, mask)
    groups = []
    visited = set()
    for v in tree:
        if v not in visited:
            group = []
            stack = [v]
            while stack:
                v = stack.pop()
                if v not in visited:
                    group.append(v)
                    visited.add(v)
                    for v2 in tree[v]:
                        stack.append(v2)
            groups.append(group)
    return groups


def components_map(edges, mask=None):
    # type: (np.ndarray, list) -> dict
    components = connected_components(edges, mask)
    c = {}
    for i, v in enumerate(components):
        for j in v:
            c[j] = i
    return c
    

def adjacency_matrix(tree):
    n = len(tree)
    adj = np.zeros((n, n))
    for v in tree:
        for v2 in tree[v]:
            adj[v][v2] = 1
    return adj, n


def fitness(allEdges, selectedEdges):
    m = len(allEdges)

    if fitness.cache is None:
        tree = construct_tree(allEdges)
        A, n = adjacency_matrix(tree)
        fitness.cache = tree, A, n
    else:
        tree, A, n = fitness.cache

    groups = components_map(allEdges, selectedEdges)

    q = 0
    for i in range(n):
        for j in range(n):
            if groups[i] == groups[j]:
                q += A[i][j] - len(tree[i]) * len(tree[j]) / (2 * m)

    return q / (2 * m)

fitness.cache = None