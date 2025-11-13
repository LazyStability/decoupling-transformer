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

GraphChils::GraphChils(): solver(chils_initialize()) {
    std::cout << "Initialise Graph" << std::endl;
}
GraphChils::~GraphChils() {
    std::cout << "Destroy Graph" << std::endl;
    chils_release(solver);
}
int GraphChils::add_vertex(long long weight) {
    std::cout << "Chils add graph weight: " << weight << std::endl;
    chils_add_vertex(solver, weight);
    return num_of_vertex++;
}
void GraphChils::add_edge(int first_vertex, int second_vertex) {
    std::cout << "Chils add edge between: " << second_vertex << " "
              << first_vertex << std::endl;
    chils_add_edge(solver, second_vertex, first_vertex);
    num_of_edges++;
}
bool GraphChils::empty() const {
    return num_of_vertex == 0;
}
void GraphChils::full_run(double time_limit, int n_solutions,
                          unsigned int seed) const {
    std::cout << "Chils started" << std::endl;
    chils_run_full(solver, time_limit, n_solutions, seed);
    std::cout << "Chils finished" << std::endl;
    int size = chils_solution_get_size(solver);
    int* arr = chils_solution_get_independent_set(solver);
    std::cout << chils_solution_get_size(solver) << std::endl;
    best_solution.assign(arr, arr + size);
}
void GraphChils::local_run(double time_limit, unsigned int seed) const {
    std::cout << "Chils started" << std::endl;
    chils_run_local_search_only(solver, time_limit, seed);
    std::cout << "Chils finished" << std::endl;
    int size = chils_solution_get_size(solver);
    std::cout << "Size: " << size << std::endl;
    int* arr = chils_solution_get_independent_set(solver);
    std::cout << "Weight: " << chils_solution_get_weight(solver) << std::endl;
    std::cout << "Vertex one: "
              << chils_solution_get_vertex_configuration(solver, 0);
    std::cout << "Vertex two: "
              << chils_solution_get_vertex_configuration(solver, 1);
    std::cout << "Vertex three: "
              << chils_solution_get_vertex_configuration(solver, 2);
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
    std::cout << "Adding edge" << std::endl;
    chils_add_edge(test_solver, 0, 2); // Edge {2, 1}
    std::cout << "Adding edge" << std::endl;
    chils_add_edge(test_solver, 0, 3); // Edge {2, 1}
    std::cout << "Adding edge" << std::endl;

    // Local search is recommended for small time limits (< 5min)
    // chils_run_local_search_only(solver, 1.0, 0);

    // CHILS is recommended for larger time limits (> 5min)
    chils_run_full(test_solver, 1.0, 8, 0);
    std::cout << "solution found" << std::endl;

    std::cout << chils_solution_get_weight(test_solver) << std::endl;

    chils_release(test_solver);
}

long long GraphChils::get_best_solution_weight() const {
    return chils_solution_get_weight(solver);
}
