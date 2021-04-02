import copy
import numpy as np
# from Heuristics.GreedyCycle import greedy_cycle
# from Heuristics.CreateDistanceMatrix import *
# from Heuristics.Visualize import plot_results
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


def get_best_edges_swap(cycle, distance_matrix):
    best_cycle_with_swap = None
    best_swap_length = np.inf
    for idx_1 in range(len(cycle)):
        if idx_1 - 1 < 0:
            edge_1 = (-1, idx_1)
        else:
            edge_1 = (idx_1 - 1, idx_1)
        for idx_2 in range(len(cycle)):
            if idx_2 - 1 < 0:
                edge_2 = (-1, idx_2)
            else:
                edge_2 = (idx_2 - 1, idx_2)
            if edge_1 != edge_2 and edge_1[1] != edge_2[0]:
                cycle_with_swap = copy.deepcopy(cycle)
                cycle_with_swap[edge_1[0]+1:edge_2[0]+1] = cycle_with_swap[edge_1[0]+1:edge_2[0]+1][::-1]
                cycle_with_swap_length = cycle_length(cycle_with_swap, distance_matrix)
                if best_swap_length - cycle_with_swap_length > 0:
                    best_swap_length = cycle_with_swap_length
                    best_cycle_with_swap = cycle_with_swap
    return best_swap_length, best_cycle_with_swap


def get_best_vertices_swap(cycle, distance_matrix):
    best_cycle_with_swap = None
    best_swap_length = np.inf
    for idx_1 in range(len(cycle)):
        for idx_2 in range(idx_1, len(cycle)):
            if idx_1 != idx_2:
                cycle_with_swap = copy.deepcopy(cycle)
                cycle_with_swap[idx_1], cycle_with_swap[idx_2] = cycle_with_swap[idx_2], cycle_with_swap[idx_1]
                cycle_with_swap_length = cycle_length(cycle_with_swap, distance_matrix)
                if best_swap_length - cycle_with_swap_length > 0:
                    best_swap_length = cycle_with_swap_length
                    best_cycle_with_swap = cycle_with_swap
    return best_swap_length, best_cycle_with_swap


def improve_cycles(cycle_1, cycle_2, distance_matrix, method):

    cycle_stop = False
    pick_cycle = 0

    while not cycle_stop:

        best_swap_vertices_or_edges = (None, None)

        if pick_cycle % 2 == 0:
            cycle = cycle_1
            other_cycle = cycle_2
        else:
            cycle = cycle_2
            other_cycle = cycle_1

        if method == 0:
            best_swap_vertices_or_edges = get_best_vertices_swap(cycle, distance_matrix)
        elif method == 1:
            best_swap_vertices_or_edges = get_best_edges_swap(cycle, distance_matrix)

        best_swap_between_length, best_swap_between_cycles = \
            get_best_vertices_swap_between_cycles(cycle_1, cycle_2, distance_matrix)

        if (best_swap_vertices_or_edges[0] + cycle_length(other_cycle, distance_matrix)) - best_swap_between_length > 0:
            best_length = best_swap_between_length
            best_cycles = best_swap_between_cycles
        else:
            best_length = best_swap_vertices_or_edges[0] + cycle_length(other_cycle, distance_matrix)
            if pick_cycle % 2 == 0:
                best_cycles = (best_swap_vertices_or_edges[1], other_cycle)
            else:
                best_cycles = (other_cycle, best_swap_vertices_or_edges[1])

        if (cycle_length(cycle_1, distance_matrix) + cycle_length(cycle_2, distance_matrix)) - best_length > 0:
            cycle_1, cycle_2 = best_cycles
        else:
            cycle_stop = True

        pick_cycle += 1

    return cycle_1, cycle_2


def get_best_vertices_swap_between_cycles(cycle_1, cycle_2, distance_matrix):
    best_cycles_with_swap = (None, None)
    best_swap_length_sum = np.inf
    for idx_1 in range(len(cycle_1)):
        for idx_2 in range(len(cycle_2)):
            cycle_1_with_swap = copy.deepcopy(cycle_1)
            cycle_2_with_swap = copy.deepcopy(cycle_2)
            cycle_1_with_swap[idx_1], cycle_2_with_swap[idx_2] = cycle_2_with_swap[idx_2], cycle_1_with_swap[idx_1]
            cycle_1_with_swap_length = cycle_length(cycle_1_with_swap, distance_matrix)
            cycle_2_with_swap_length = cycle_length(cycle_2_with_swap, distance_matrix)
            if best_swap_length_sum - (cycle_1_with_swap_length + cycle_2_with_swap_length) > 0:
                best_swap_length_sum = cycle_1_with_swap_length + cycle_2_with_swap_length
                best_cycles_with_swap = (cycle_1_with_swap, cycle_2_with_swap)
    return best_swap_length_sum, best_cycles_with_swap


def steepest_local_search(cycle_1, cycle_2, distance_matrix, method):
    """

    :param cycle_1_initial:
    :param cycle_2_initial:
    :param distance_matrix:
    :param method: 1 -> exchanges of edges within cycles and exchanges of verices between cycles,
    0 -> exchanges of verices within cycles and exchanges of verices between cycles
    :return:
    """

    cycle_1, cycle_2 = improve_cycles(cycle_1, cycle_2, distance_matrix, method)

    return cycle_1, cycle_2


# coordinates_a = load_data_from_file('../Heuristics/kroA100.tsp')
# distance_matrix_a = create_distance_matrix('../Heuristics/kroA100.tsp')
# cycle_1, cycle_2 = greedy_cycle(distance_matrix_a, start_vertex_1=None)
# print(cycle_length(cycle_1, distance_matrix_a))
# print(cycle_length(cycle_2, distance_matrix_a))
# xs = [coord[0] for coord in coordinates_a]
# ys = [coord[1] for coord in coordinates_a]
# plot_results(xs, ys, cycle_1, cycle_2)
# cycle_1_improved, cycle_2_improved = steepest_local_search(cycle_1, cycle_2, distance_matrix_a, method=0)
# print(cycle_length(cycle_1_improved, distance_matrix_a))
# print(cycle_length(cycle_2_improved, distance_matrix_a))
# plot_results(xs, ys, cycle_1_improved, cycle_2_improved)
