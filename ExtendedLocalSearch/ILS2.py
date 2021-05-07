import copy
import math
import time
import numpy as np
from Common.CreateDistanceMatrix import load_data_from_file, create_distance_matrix
from Common.Visualize import plot_results
from ExtendedLocalSearch.GreedyCycleForILS2 import greedy_cycle_for_ils2
from Heuristics.GreedyCycle import greedy_cycle
from ImprovedLocalSearch.SteepestList import ls_steepest_list
from LocalSearch.RandomWalk import cycle_length


def ils2_perturbation(cycle_1, cycle_2, distance_matrix):
    k = math.ceil(distance_matrix.shape[0]*0.2 / 2.) * 2
    vertices_to_remove_1 = np.random.choice(cycle_1, int(k/2), replace=False)
    vertices_to_remove_2 = np.random.choice(cycle_2, int(k/2), replace=False)
    cycle_1_with_perturbation = [vertex for vertex in cycle_1 if vertex not in vertices_to_remove_1]
    cycle_2_with_perturbation = [vertex for vertex in cycle_2 if vertex not in vertices_to_remove_2]
    return cycle_1_with_perturbation, cycle_2_with_perturbation


def ils2_method(cycle_1, cycle_2, distance_matrix, with_ls=True, runtime=5):
    cycle_1_with_updates = copy.deepcopy(cycle_1)
    cycle_2_with_updates = copy.deepcopy(cycle_2)
    best_cycles = (cycle_1, cycle_2)
    best_cycles_length = cycle_length(cycle_1, distance_matrix) + cycle_length(cycle_2, distance_matrix)
    start_time = time.time()

    cycle_1_with_updates, cycle_2_with_updates = ls_steepest_list(cycle_1_with_updates, cycle_2_with_updates, distance_matrix)

    while time.time() - start_time < runtime:
        cycle_1_with_updates, cycle_2_with_updates = ils2_perturbation(cycle_1_with_updates, cycle_2_with_updates, distance_matrix)
        cycle_1_with_updates, cycle_2_with_updates = greedy_cycle_for_ils2(cycle_1_with_updates, cycle_2_with_updates, distance_matrix)
        if with_ls:
            cycle_1_with_updates, cycle_2_with_updates = ls_steepest_list(cycle_1_with_updates, cycle_2_with_updates,
                                                                          distance_matrix)
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
# cycle_1_improved, cycle_2_improved = ils2_method(cycle_1, cycle_2, distance_matrix_a, False, 5)
# print(cycle_length(cycle_1_improved, distance_matrix_a))
# print(cycle_length(cycle_2_improved, distance_matrix_a))
# plot_results(xs, ys, cycle_1_improved, cycle_2_improved)
