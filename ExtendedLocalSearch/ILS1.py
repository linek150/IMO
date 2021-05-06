import copy
import random
import time

import numpy as np

from Common.CreateDistanceMatrix import load_data_from_file, create_distance_matrix
from Common.Visualize import plot_results
from Heuristics.GreedyCycle import greedy_cycle
from LocalSearch.RandomWalk import cycle_length
from LocalSearch.SteepestLS import ls_steepest


def find_closest_vertices(distance_matrix, vertex, k):
    k_closest = np.argpartition(distance_matrix[vertex], k)[:k]
    return k_closest


def generate_random_pairs(vertices_list):

    def pop_random(lst):
        idx = random.randrange(0, len(lst))
        return lst.pop(idx)

    pairs = []
    vertices_list = vertices_list.tolist()
    while vertices_list:
        rand1 = pop_random(vertices_list)
        rand2 = pop_random(vertices_list)
        pair = rand1, rand2
        pairs.append(pair)
    return pairs


def get_random_vertices_swap_between_cycles(cycle_1, cycle_2, vertex_1_idx, vertex_2_idx):
    cycle_1_with_swap = copy.deepcopy(cycle_1)
    cycle_2_with_swap = copy.deepcopy(cycle_2)
    cycle_1_with_swap[vertex_1_idx], cycle_2_with_swap[vertex_2_idx] = cycle_2_with_swap[vertex_2_idx], cycle_1_with_swap[vertex_1_idx]
    return cycle_1_with_swap, cycle_2_with_swap


def get_random_vertices_swap(cycle, v_1_idx, v2_idx):
    cycle_with_swap = copy.deepcopy(cycle)
    cycle_with_swap[v_1_idx], cycle_with_swap[v2_idx] = cycle_with_swap[v2_idx], cycle_with_swap[v_1_idx]
    return cycle_with_swap


def get_random_edges_swap(cycle, edge_1, edge_2):
    cycle_with_swap = copy.deepcopy(cycle)
    cycle_with_swap[edge_1[0] + 1:edge_2[0] + 1] = cycle_with_swap[edge_1[0] + 1:edge_2[0] + 1][::-1]
    return cycle_with_swap


def generate_small_perturbation(cycle_1, cycle_2, vertex, distance_matrix, k):
    cycle_1_with_swaps = copy.deepcopy(cycle_1)
    cycle_2_with_swaps = copy.deepcopy(cycle_2)
    k_closest = find_closest_vertices(distance_matrix, vertex, k)
    random_vertices_pairs = generate_random_pairs(k_closest)

    for v_1, v_2 in random_vertices_pairs[:int(len(random_vertices_pairs)/2)]:
        if v_1 in cycle_1_with_swaps and v_2 in cycle_1_with_swaps:
            # Swap edges in cycle_1
            v_1_idx = cycle_1_with_swaps.index(v_1)
            edge_1 = (v_1_idx, v_1_idx+1)
            v_2_idx = cycle_1_with_swaps.index(v_2)
            edge_2 = (v_2_idx, v_2_idx + 1)
            if not edge_1 == edge_2 and not edge_1[1] == edge_2[0]:
                cycle_1_with_swaps = get_random_edges_swap(cycle_1_with_swaps, edge_1, edge_2)
        elif v_1 in cycle_2_with_swaps and v_2 in cycle_2_with_swaps:
            # Swap edges in cycle_2
            v_1_idx = cycle_2_with_swaps.index(v_1)
            edge_1 = (v_1_idx, v_1_idx+1)
            v_2_idx = cycle_2_with_swaps.index(v_2)
            edge_2 = (v_2_idx, v_2_idx + 1)
            if not edge_1 == edge_2 and not edge_1[1] == edge_2[0]:
                cycle_2_with_swaps = get_random_edges_swap(cycle_2_with_swaps, edge_1, edge_2)

    for v_1, v_2 in random_vertices_pairs[int(len(random_vertices_pairs)/2):]:
        if v_1 in cycle_1_with_swaps and v_2 in cycle_1_with_swaps:
            # Swap vertices in cycle_1
            cycle_1_with_swaps = get_random_vertices_swap(cycle_1_with_swaps, cycle_1_with_swaps.index(v_1),
                                                          cycle_1_with_swaps.index(v_2))
        elif v_1 in cycle_2_with_swaps and v_2 in cycle_2_with_swaps:
            # Swap vertices in cycle_2
            cycle_2_with_swaps = get_random_vertices_swap(cycle_2_with_swaps, cycle_2_with_swaps.index(v_1),
                                                          cycle_2_with_swaps.index(v_2))
        elif v_1 in cycle_1_with_swaps and v_2 in cycle_2_with_swaps:
            # Swap vertices between cycles
            cycle_1_with_swaps, cycle_2_with_swaps = get_random_vertices_swap_between_cycles(
                cycle_1_with_swaps, cycle_2_with_swaps, cycle_1_with_swaps.index(v_1),
                cycle_2_with_swaps.index(v_2))
        elif v_1 in cycle_2_with_swaps and v_2 in cycle_1_with_swaps:
            # Swap vertices between cycles
            cycle_1_with_swaps, cycle_2_with_swaps = get_random_vertices_swap_between_cycles(
                cycle_1_with_swaps, cycle_2_with_swaps, cycle_1_with_swaps.index(v_2),
                cycle_2_with_swaps.index(v_1))

    return cycle_1_with_swaps, cycle_2_with_swaps


def ils1_perturbation(cycle_1, cycle_2, distance_matrix):

    k = 8
    vertex = np.random.choice(distance_matrix.shape[0], 1)[0]
    cycle_1, cycle_2 = generate_small_perturbation(cycle_1, cycle_2, vertex, distance_matrix, k)

    return cycle_1, cycle_2


def ils1_method(cycle_1, cycle_2, distance_matrix, runtime):
    cycle_1_with_updates = copy.deepcopy(cycle_1)
    cycle_2_with_updates = copy.deepcopy(cycle_2)
    best_cycles = (cycle_1, cycle_2)
    best_cycles_length = cycle_length(cycle_1, distance_matrix) + cycle_length(cycle_2, distance_matrix)
    start_time = time.time()
    while time.time() - start_time < runtime:
        cycle_1_with_updates, cycle_2_with_updates = ils1_perturbation(cycle_1_with_updates, cycle_2_with_updates, distance_matrix)
        cycle_1_with_updates, cycle_2_with_updates = ls_steepest(cycle_1_with_updates, cycle_2_with_updates, distance_matrix)
        cycle_1_with_updates, cycle_2_with_updates = cycle_1_with_updates.tolist(), cycle_2_with_updates.tolist()
        cycles_length = cycle_length(cycle_1_with_updates, distance_matrix) + cycle_length(cycle_2_with_updates, distance_matrix)
        if cycles_length < best_cycles_length:
            best_cycles = (cycle_1_with_updates, cycle_2_with_updates)
            best_cycles_length = cycles_length
    return best_cycles


# coordinates_a = load_data_from_file('../Heuristics/kroA100.tsp')
# distance_matrix_a = create_distance_matrix('../Heuristics/kroA100.tsp')
# cycle_1, cycle_2 = greedy_cycle(distance_matrix_a, start_vertex_1=None)
# print(cycle_length(cycle_1, distance_matrix_a))
# print(cycle_length(cycle_2, distance_matrix_a))
# xs = [coord[0] for coord in coordinates_a]
# ys = [coord[1] for coord in coordinates_a]
# plot_results(xs, ys, cycle_1, cycle_2)
# cycle_1_improved, cycle_2_improved = ils1_method(cycle_1, cycle_2, distance_matrix_a, 5)
# print(cycle_length(cycle_1_improved, distance_matrix_a))
# print(cycle_length(cycle_2_improved, distance_matrix_a))
# plot_results(xs, ys, cycle_1_improved, cycle_2_improved)
