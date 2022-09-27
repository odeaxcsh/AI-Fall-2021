''' 
this file is not part of solution
it's soupposed to be used for testing and comparing results of c++ code with networkx library
'''

import networkx

# try to import communities.py
try:
    from communities import communities as cpp_communities
except ImportError:
    print('communities.py not found')
    print('you need to run c++ code first in order to get generate results') 

# return sorted list of nodes
def load(filename):
    with open(filename, 'r') as f:
        n = int(f.readline())
        edges = []
        for line in f:
            i, j = map(int, line.split())
            if j < i:
                i, j = j, i
            edges.append((i - 1, j - 1))
    return n, list(sorted(edges))

_, edges = load('graph.txt')
# graph from edges
G = networkx.Graph(edges)

# find communities
partition = networkx.algorithms.community.greedy_modularity_communities(G)

# find madularity
modularity = networkx.algorithms.community.modularity(G, partition)

# print results
print("Modularity:", modularity)
for part in partition:
    print("Community:", part)
print()

# print c++ communities
print("C++ communities:")
for part in cpp_communities:
    print("Community:", part)

#print modularity
print("C++ code result Modularity:", networkx.algorithms.community.modularity(G, cpp_communities))

print()
print("I don't know why, but this is not equal to c++ code result")
print("Actually, c++ code found better modularity")