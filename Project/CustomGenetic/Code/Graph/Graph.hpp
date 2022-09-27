#if !defined(GRAPH_HPP)
#define GRAPH_HPP

#include <map>
#include <unordered_set>
#include <set>

namespace graph
{

class Graph
{
public:
    Graph()
    {
        
    }

    void addEdge(int u, int v)
    {
        if(!hasEdge(u, v) && u != v) {
            ++numberOfEdges;
            adj[u].insert(v);
            adj[v].insert(u);
        }
    }

    int degree(int u) const
    {
        return adj.at(u).size();
    }

    int edgeNumber() const
    {
        return numberOfEdges;
    }

    int size() const
    {
        return adj.size();
    }

    // return set of all edges
    std::set<std::pair<int, int>> getEdges() const
    {
        std::set<std::pair<int, int>> edges;
        for(auto [u, adj] : adj) {
            for(auto v : adj) {
                if(u != v && edges.find({v, u}) == edges.end()) {
                    edges.insert({u, v});
                }
            }
        }
        return edges;
    }

    std::unordered_set<int>& getAdj(int v)
    {
        return adj[v];
    }

    void addVertex(int v)
    {
        adj[v];
    }
    
    bool hasEdge(int u, int v)
    {
        return adj[u].end() != adj[u].find(v);
    }

    auto getVertices()
    {
        return adj;
    }

private:
    std::map<int, std::unordered_set<int>> adj;
    int numberOfEdges = 0;
};

}

#endif