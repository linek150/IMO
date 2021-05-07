import numpy as np


def greedy_cycle_for_ils2(cycle_1, cycle_2, distance_matrix):
    set_difference = set(range(distance_matrix.shape[0])) - set(cycle_1) - set(cycle_2)
    unused_vertex = list(set_difference)
    which_cycle = 0
    while unused_vertex:
        cycle = cycle_1 if which_cycle % 2 == 0 else cycle_2
        smallest_length_increase = np.inf
        best_insert_idx = -1
        best_vertex = -1
        for split_idx in range(len(cycle)):
            curr_distance = distance_matrix[cycle[split_idx - 1], cycle[split_idx]]
            for vertex in unused_vertex:
                distance1 = distance_matrix[vertex, cycle[split_idx]]
                distance2 = distance_matrix[vertex, cycle[split_idx - 1]]
                new_distance = distance1 + distance2
                if new_distance - curr_distance < smallest_length_increase:
                    smallest_length_increase = new_distance - curr_distance
                    best_insert_idx = split_idx
                    best_vertex = vertex
        cycle.insert(best_insert_idx, best_vertex)
        unused_vertex.remove(best_vertex)
        which_cycle += 1
    return cycle_1, cycle_2
