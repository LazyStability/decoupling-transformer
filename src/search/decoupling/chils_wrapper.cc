#include "chils_wrapper.h"

#include "chils.h"

#include <iostream>

extern "C" {
    // C Function call
    long long chils_solution_get_weight(void*);
    int* chils_solution_get_independent_set(void*);
    void chils_run_full(void*, double, int, unsigned int);
    void chils_run_local_search_only(void*, double, unsigned int);
    int chils_solution_get_size(void*);
    void* chils_initialize();
    void chils_release(void*);
    void chils_add_edge(void*, int, int);
    int chils_add_vertex(void*, long long);
    int chils_solution_get_vertex_configuration(void*, int);
}

GraphChils::GraphChils()
    : num_of_vertex(0), num_of_edges(0), solver(chils_initialize()) {}
GraphChils::~GraphChils() {
    chils_release(solver);
}
int GraphChils::add_vertex(long long weight) {
    chils_add_vertex(solver, weight);
    return num_of_vertex++;
}
void GraphChils::add_edge(int first_vertex, int second_vertex) {
    chils_add_edge(solver, first_vertex, second_vertex);
    num_of_edges++;
}
bool GraphChils::empty() const {
    return num_of_vertex == 0;
}
void GraphChils::full_run(double time_limit, int n_solutions,
                          unsigned int seed) const {
    chils_run_full(solver, time_limit, n_solutions, seed);
    int size = chils_solution_get_size(solver);
    int* arr = chils_solution_get_independent_set(solver);
    best_solution.assign(arr, arr + size);
}
void GraphChils::local_run(double time_limit, unsigned int seed) const {
    chils_run_local_search_only(solver, time_limit, seed);
    int size = chils_solution_get_size(solver);
    int* arr = chils_solution_get_independent_set(solver);

    best_solution.assign(arr, arr + size);
}

long long GraphChils::get_best_solution_weight() const {
    return chils_solution_get_weight(solver);
}
int GraphChils::get_best_solution_size() const {
    return chils_solution_get_size(solver);
}
int GraphChils::get_num_of_vertex() const {
    return num_of_vertex;
}
