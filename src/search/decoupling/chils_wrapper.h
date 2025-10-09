#ifndef CHILS_WRAPPER_H
#define CHILS_WRAPPER_H

#include <vector>

class GraphChils {
public:
    mutable std::vector<int> best_solution;

    GraphChils();
    ~GraphChils();
    GraphChils(const GraphChils& graph) = delete;
    GraphChils& operator=(const GraphChils& graph) = delete;
    bool empty() const;
    int add_vertex(long long weight);
    void add_edge(int first_vertex, int second_vertex);
    void full_run(double time_limit, int n_solutions,
                  unsigned int seed) const;
    void local_run(double time_limit, unsigned int seed) const;
    long long get_best_solution_weight() const;

 private:
    int num_of_vertex;
    int num_of_edges;
    void* solver;
};
#endif
