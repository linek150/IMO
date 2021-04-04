import numpy as np
import time
import copy
# from Heuristics.CreateDistanceMatrix import *
# from Heuristics.Visualize import plot_results
# from Heuristics.GreedyCycle import greedy_cycle
# from Heuristics.NearestNeighbor import nearest_neighbor_method


def cycle_length(cycle, distance_matrix):
    length = 0
    lengths = []
    for idx in range(len(cycle)):
        if idx - 1 < 0:
            length += distance_matrix[cycle[-1]][cycle[idx]]
            lengths.append(distance_matrix[cycle[-1]][cycle[idx]])
        else:
            length += distance_matrix[cycle[idx-1]][cycle[idx]]
            lengths.append(distance_matrix[cycle[idx-1]][cycle[idx]])
    return length


def get_random_vertices_swap_between_cycles(cycle_1, cycle_2, distance_matrix):
    vertex_1_idx = np.random.choice(len(cycle_1), 1)[0]
    vertex_2_idx = np.random.choice(len(cycle_2), 1)[0]
    cycle_1_with_swap = copy.deepcopy(cycle_1)
    cycle_2_with_swap = copy.deepcopy(cycle_2)
    cycle_1_with_swap[vertex_1_idx], cycle_2_with_swap[vertex_2_idx] = cycle_2_with_swap[vertex_2_idx], cycle_1_with_swap[vertex_1_idx]
    cycle_1_with_swap_length = cycle_length(cycle_1_with_swap, distance_matrix)
    cycle_2_with_swap_length = cycle_length(cycle_2_with_swap, distance_matrix)
    return cycle_1_with_swap_length + cycle_2_with_swap_length, (cycle_1_with_swap, cycle_2_with_swap)


def get_random_vertices_swap(cycle, distance_matrix):
    vertices_to_swap_indices = np.random.choice(len(cycle), 2, replace=False)
    cycle_with_swap = copy.deepcopy(cycle)
    cycle_with_swap[vertices_to_swap_indices[0]], cycle_with_swap[vertices_to_swap_indices[1]] = \
        cycle_with_swap[vertices_to_swap_indices[1]], cycle_with_swap[vertices_to_swap_indices[0]]
    cycle_with_swap_length = cycle_length(cycle_with_swap, distance_matrix)
    return cycle_with_swap_length, cycle_with_swap


def get_random_edges_swap(cycle, distance_matrix):
    edge_1 = np.random.choice(len(cycle), 2, replace=False)
    edge_2 = np.random.choice(len(cycle), 2, replace=False)
    while np.array_equal(edge_1, edge_2) or (edge_1[1] == edge_2[0]):
        edge_1 = np.random.choice(len(cycle), 2, replace=False)
        edge_2 = np.random.choice(len(cycle), 2, replace=False)
    cycle_with_swap = copy.deepcopy(cycle)
    cycle_with_swap[edge_1[0] + 1:edge_2[0] + 1] = cycle_with_swap[edge_1[0] + 1:edge_2[0] + 1][::-1]
    cycle_with_swap_length = cycle_length(cycle_with_swap, distance_matrix)
    return cycle_with_swap_length, cycle_with_swap


def improve_cycles_randomly(cycle_1, cycle_2, distance_matrix, runtime):

    best_found_cycles = (cycle_1, cycle_2)

    cycle_stop = False
    pick_cycle = 0
    start = time.time()

    while not cycle_stop:

        if pick_cycle % 2 == 0:
            cycle = cycle_1
        else:
            cycle = cycle_2

        pick_method = np.random.choice(3, 1)[0]

        if pick_method == 0:
            best_swap_vertices = get_random_vertices_swap(cycle, distance_matrix)
            if pick_cycle % 2 == 0:
                cycle_1 = best_swap_vertices[1]
            else:
                cycle_2 = best_swap_vertices[1]
        elif pick_method == 1:
            best_swap_edges = get_random_edges_swap(cycle, distance_matrix)
            if pick_cycle % 2 == 0:
                cycle_1 = best_swap_edges[1]
            else:
                cycle_2 = best_swap_edges[1]
        else:
            best_swap_between_length, best_swap_between_cycles = \
                get_random_vertices_swap_between_cycles(cycle_1, cycle_2, distance_matrix)
            cycle_1, cycle_2 = best_swap_between_cycles

        if (cycle_length(best_found_cycles[0], distance_matrix) + cycle_length(best_found_cycles[1], distance_matrix)) - \
                (cycle_length(cycle_1, distance_matrix) + cycle_length(cycle_2, distance_matrix)) > 0:
            best_found_cycles = (cycle_1, cycle_2)

        pick_cycle += 1

        if (time.time() - start) >= runtime:
            cycle_stop = True

    return best_found_cycles


def random_local_search(cycle_1, cycle_2, distance_matrix, runtime):

    cycle_1, cycle_2 = improve_cycles_randomly(cycle_1, cycle_2, distance_matrix, runtime)

    return cycle_1, cycle_2


# coordinates_a = load_data_from_file('../Heuristics/kroA100.tsp')
# distance_matrix_a = create_distance_matrix('../Heuristics/kroA100.tsp')
# cycle_1, cycle_2 = greedy_cycle(distance_matrix_a, start_vertex_1=None)
# print(cycle_length(cycle_1, distance_matrix_a))
# print(cycle_length(cycle_2, distance_matrix_a))
# xs = [coord[0] for coord in coordinates_a]
# ys = [coord[1] for coord in coordinates_a]
# plot_results(xs, ys, cycle_1, cycle_2)
# cycle_1_improved, cycle_2_improved = random_local_search(cycle_1, cycle_2, distance_matrix_a, runtime=5)
# print(cycle_length(cycle_1_improved, distance_matrix_a))
# print(cycle_length(cycle_2_improved, distance_matrix_a))
# plot_results(xs, ys, cycle_1_improved, cycle_2_improved)
