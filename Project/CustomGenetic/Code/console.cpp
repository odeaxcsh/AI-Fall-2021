#include "Genetic/GeneticAlgorithm.hpp"
#include "Random/Random.cpp"

#include "Solution1/Algorithm.cpp"

#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>

#include <sstream>

std::ostringstream toDotFormat(graph::Graph *problem, const std::vector<int> &color)
{
    static std::vector<const char *> colorsMap = {
        "red", "green", "blue", "yellow", "orange", "purple", "brown", "pink", "gray", "cyan", "darkred", "darkgreen", "darkblue", "darkyellow"
    };
    
    std::ostringstream dot;
    dot << "graph G {\n";
    for (auto [i, _] : problem->getVertices()) {
        dot << "    " << i << " [label=\"" << i << "\", color=\"" << colorsMap[color[i]] << "\"];\n";
    }

    for (auto [i, j] : problem->getEdges()) {
        if(color[i] == color[j]) {
            dot << "    " << i << " -- " << j << " [color=\"" << colorsMap[color[i]] << "\"];\n";
        } else {
            dot << "    " << i << " -- " << j << " [color=\"black\", style=\"dotted\"];\n";
        }
    }
    dot << "}\n";
    return dot;
}

bool readGraphFromFile(graph::Graph *problem, const char *path)
{
    std::ifstream ifile(path);
    if(!ifile.is_open()) {
        return false;
    }
    int n;
    ifile >> n;
    for(int i = 0; i < n; ++i) {
        problem->addVertex(i);
    }

    //till the end of file
    while(!ifile.eof()) {
        int i, j;
        ifile >> i >> j;
        problem->addEdge(i - 1, j - 1);
    }
    return true;
}

bool readGraphFromStdin(graph::Graph *problem)
{

    int n;
    std::cout << "Enter number of vertices: ";
    std::cin >> n;
    for(int i = 0; i < n; ++i) {
        problem->addVertex(i);
    }

    int m;
    std::cout << "Enter number of edges: ";
    std::cin >> m;
    //till the end of file
    while(m --> 0) {
        int i, j;
        std::cout << "Enter edge: ";
        std::cin >> i >> j;
        problem->addEdge(i - 1, j - 1);
    }

    return true;
}

int _main()
{
    using solution solution1;

    graph::Graph *problem = new graph::Graph();

    if(!readGraphFromFile(problem, "graph.txt")) {
        bool valid = false;
        while(!valid) {
            std::cout << "Enter graph file name or stdin to enter graph manually: ";
            std::string path;
            std::cin >> path;
            if(path == "stdin") {
                readGraphFromStdin(problem);
            } else if(readGraphFromFile(problem, path.c_str())) {
                valid = true;
            } else {
                std::cout << "Invalid file name. Try again.\n";
            }
        }
    }

    std::cout << "File loaded" << std::endl;

    // history of best fitness of each generation
    std::vector<double> fitnesses;

    // genetic algorithm with following parameters:
    // number of generations: 100
    // population size: 100
    // mutation rate: 0.1
    // crossover rate: 0.9
    genetic::GeneticAlgorithm<Chromosome> algorithm(new Algorithm(problem), 0.9, 0.9, 100, 100);
    while(not algorithm.finished()) {
        Chromosome *chromosome = algorithm.bestFit();
        fitnesses.push_back(chromosome->fitness());

        std::cout << "Fitness: " << chromosome->fitness() << std::endl;
        std::cout << "Number of groups: " << chromosome->numberOfGroups << std::endl;

        // if fitness is same for 10 generations, stop
        if(fitnesses.size() > 10 and fitnesses.back() == fitnesses[fitnesses.size() - 10]) {
            fitnesses.erase(fitnesses.begin() + fitnesses.size() - 9, fitnesses.end());
            break;
        }

        // run genetic algorithm and print ellapsed time
        auto start = std::chrono::high_resolution_clock::now();
        algorithm.nextGeneration();
        auto end = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double> diff = end - start;
        std::cout << "[New generation generated in : " << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count() << "ms]" << std::endl;
        std::cout << std::endl;
    }

    Chromosome  *chromosome = algorithm.bestFit();
    std::cout << std::endl;
    
    // list of colors
    std::vector<const char *> colors = {
        "red", "blue", "green", "black", "yellow", "white", "purple", "pink", "brown", "orange", "gray", "cyan", "magenta", "steelblue"
    };

    // print out solution
    std::ofstream file("graph.dot");
    std::vector<int> color(problem->size());
    for(int i = 0; i < problem->size(); ++i) {
        color[i] = (*chromosome)[i];
    }
    file << toDotFormat(problem, color).str();
    file.close();

    std::cout << "output written to graph.dot" << std::endl;
    std::cout << "use graphviz to visualize graph" << std::endl;

    // try to visualize graph
    if(std::system("dot -V") == 0) {
        std::system("dot -Tpng graph.dot -o graph.png");
        std::system("xdg-open graph.png");
    } else {
        std::cout << "graphviz not found" << std::endl;
        std::cout << "use this website for online graph preview: http://magjac.com/graphviz-visual-editor/" << std::endl;
    }

    std::vector<std::vector<int>> communities(chromosome->numberOfGroups);
    for(int i = 0; i < problem->size(); ++i) {
        communities[(*chromosome)[i]].push_back(i);
    }

    // print out communities
    std::cout << "Communities: " << std::endl;
    for(int i = 0; i < chromosome->numberOfGroups; ++i) {
        std::cout << "Community " << i << ": ";
        for(std::size_t j = 0; j < communities[i].size(); ++j) {
            std::cout << communities[i][j] << " ";
        }
        std::cout << std::endl;
    }

    // check if user wants to compare  results with other algorithm
    std::cout << "Do you want to campare results with python's networX library? (y/n)" << std::endl;
    char answer;
    std::cin >> answer;
    if(answer == 'n') {
        return 0;
    }
    
    // print out communities as a python variable
    std::ofstream python("communities.py");
    python << "communities = [\n";
    for(auto community : communities) {
        python << "\t[";
        for(auto vertex : community) {
            python << vertex << ", ";
        }
        python << "], \n";
    }
    python << "]\n";
    python.close();

    std::cout << "Running python script..." << std::endl;
    int result = std::system("python3 compareResults.py");
    if(result == 0) {
        std::cout << "Done." << std::endl;
    } else {
        std::cout << "something unexpected happened" << std::endl;
        std::cout << "probably python3 or networkx is not installed" << std::endl;
    }
    return 0;
}

// executes _main and prints ellapsed time
int main()
{
    auto start = std::chrono::steady_clock::now();
    auto result = _main();
    auto end = std::chrono::steady_clock::now();
    std::cout << "[Program finished : " << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count() << "ms]" << std::endl;
    return result;
}