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
void GraphChils::test_run() {
    void* test_solver = chils_initialize();

    // Creating a graph: 15---20---15

    std::cout << "Starting run" << std::endl;
    chils_add_vertex(test_solver, 1); // Vertex 0
    std::cout << "Adding node weight 1" << std::endl;
    chils_add_vertex(test_solver, 1); // Vertex 1
    std::cout << "Adding node weight 1" << std::endl;
    chils_add_vertex(test_solver, 1); // Vertex 2
    std::cout << "Adding node weight 1" << std::endl;
    chils_add_vertex(test_solver, 1); // Vertex 2
    std::cout << "Adding node weight 1" << std::endl;

    chils_add_edge(test_solver, 0, 1); // Edge {0, 2}
    std::cout << "Adding edge 0 1" << std::endl;
    chils_add_edge(test_solver, 0, 2); // Edge {2, 1}
    std::cout << "Adding edge 0 2" << std::endl;
    chils_add_edge(test_solver, 0, 3); // Edge {2, 1}
    std::cout << "Adding edge 0 3" << std::endl;

    // Local search is recommended for small time limits (< 5min)
    // chils_run_local_search_only(test_solver, 1.0, 0);

    // CHILS is recommended for larger time limits (> 5min)
    chils_run_full(test_solver, 1.0, 1, 0);
    std::cout << "solution found" << std::endl;

    std::cout << "Vertex one: "
              << chils_solution_get_vertex_configuration(test_solver, 0)
              << std::endl;
    std::cout << "Vertex two: "
              << chils_solution_get_vertex_configuration(test_solver, 1)
              << std::endl;
    std::cout << "Vertex three: "
              << chils_solution_get_vertex_configuration(test_solver, 2)
              << std::endl;
    std::cout << "Vertex four: "
              << chils_solution_get_vertex_configuration(test_solver, 3)
              << std::endl;

    std::cout << chils_solution_get_weight(test_solver) << std::endl;

    chils_release(test_solver);
}

long long GraphChils::get_best_solution_weight() const {
    return chils_solution_get_weight(solver);
}
