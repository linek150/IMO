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


def check_exchange_in_cycle(cycle, vertex_idx, neighbor_idx, distance_matrix):
    cycle_with_swap = copy.deepcopy(cycle)
    edge_1 = (vertex_idx-1, vertex_idx)
    edge_2 = (neighbor_idx-1, neighbor_idx)
    if edge_1 != edge_2 and edge_1[1] != edge_2[0]:
        cycle_with_swap[edge_1[0] + 1:edge_2[0] + 1] = cycle_with_swap[edge_1[0] + 1:edge_2[0] + 1][::-1]
    cycle_with_swap_length = cycle_length(cycle_with_swap, distance_matrix)
    return cycle_with_swap, cycle_with_swap_length


def check_exchange_between_cycles(current_cycle, other_cycle, vertex_idx, neighbor_idx, distance_matrix, current_cycle_idx):
    cycle_with_swap_1 = current_cycle[:vertex_idx+1] + other_cycle[neighbor_idx:]
    cycle_with_swap_2 = other_cycle[:neighbor_idx] + current_cycle[vertex_idx+1:]
    if current_cycle_idx == 1:
        return (cycle_with_swap_1, cycle_with_swap_2), \
               cycle_length(cycle_with_swap_1, distance_matrix) + cycle_length(cycle_with_swap_2, distance_matrix)
    elif current_cycle_idx == 2:
        return (cycle_with_swap_2, cycle_with_swap_1), \
               cycle_length(cycle_with_swap_1, distance_matrix) + cycle_length(cycle_with_swap_2, distance_matrix)


def find_closest_vertices(distance_matrix, vertex, k):
    k_closest = np.argpartition(distance_matrix[vertex], k)
    return k_closest


def get_candidate_moves(current_cycle, other_cycle, vertex_idx, distance_matrix, k, current_cycle_idx):
    k_closest = find_closest_vertices(distance_matrix, current_cycle[vertex_idx], k)
    candidate_moves = []
    for neighbor in k_closest:
        if neighbor in current_cycle:
            cycle_with_swap, cycle_with_swap_length = check_exchange_in_cycle(
                current_cycle, vertex_idx, np.where(current_cycle == neighbor)[0][0], distance_matrix)
            if current_cycle_idx == 1:
                candidate_moves.append((cycle_with_swap_length + cycle_length(other_cycle, distance_matrix),
                                        (cycle_with_swap, other_cycle)))
            elif current_cycle_idx == 2:
                candidate_moves.append((cycle_with_swap_length + cycle_length(other_cycle, distance_matrix),
                                        (other_cycle, cycle_with_swap)))
        elif neighbor in other_cycle:
            cycles_with_swap, cycles_with_swap_length = check_exchange_between_cycles(
                current_cycle, other_cycle, vertex_idx, np.where(other_cycle == neighbor)[0][0],
                distance_matrix, current_cycle_idx)
            candidate_moves.append((cycles_with_swap_length, cycles_with_swap))
    candidate_moves_sorted = sorted(candidate_moves, key=lambda tup: tup[0])
    return candidate_moves_sorted


def improve_cycles(cycle_1, cycle_2, distance_matrix, k):
    for idx, vertex in enumerate(cycle_1):
        candidate_moves = get_candidate_moves(cycle_1, cycle_2, idx, distance_matrix, k, 1)
        if candidate_moves[0][0] < cycle_length(cycle_1, distance_matrix) + cycle_length(cycle_2, distance_matrix):
            cycle_1, cycle_2 = candidate_moves[0][1]
    for idx, vertex in enumerate(cycle_2):
        candidate_moves = get_candidate_moves(cycle_2, cycle_1, idx, distance_matrix, k, 2)
        if candidate_moves[0][0] < cycle_length(cycle_1, distance_matrix) + cycle_length(cycle_2, distance_matrix):
            cycle_1, cycle_2 = candidate_moves[0][1]
    return cycle_1, cycle_2


def candidate_moves_search(cycle_1, cycle_2, distance_matrix, k=10):
    """

    :param cycle_1_initial:
    :param cycle_2_initial:
    :param distance_matrix:
    :return:
    """

    cycle_1, cycle_2 = improve_cycles(cycle_1, cycle_2, distance_matrix, k)

    return cycle_1, cycle_2


# coordinates_a = load_data_from_file('../Heuristics/kroA100.tsp')
# distance_matrix_a = create_distance_matrix('../Heuristics/kroA100.tsp')
# cycle_1, cycle_2 = greedy_cycle(distance_matrix_a, start_vertex_1=None)
# print(cycle_length(cycle_1, distance_matrix_a))
# print(cycle_length(cycle_2, distance_matrix_a))
# xs = [coord[0] for coord in coordinates_a]
# ys = [coord[1] for coord in coordinates_a]
# plot_results(xs, ys, cycle_1, cycle_2)
# cycle_1_improved, cycle_2_improved = candidate_moves_search(cycle_1, cycle_2, distance_matrix_a)
# print(cycle_length(cycle_1_improved, distance_matrix_a))
# print(cycle_length(cycle_2_improved, distance_matrix_a))
# plot_results(xs, ys, cycle_1_improved, cycle_2_improved)
