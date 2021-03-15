import numpy as np
from CreateDistanceMatrix import create_distance_matrix, load_data_from_file
from Visualize import plot_results


def find_closest_vertex(distance_matrix, vertex, cycle_1, cycle_2):
    distance_matrix[vertex, cycle_1] = np.inf
    distance_matrix[vertex, cycle_2] = np.inf
    return np.argmin(distance_matrix[vertex])


def nearest_neighbor_method(distance_matrix,start_vertex_1=None):
    if start_vertex_1==None:
        start_vertex_1 = np.random.choice(distance_matrix.shape[0])
    start_vertex_2 = np.argmax(distance_matrix[start_vertex_1])
    cycle_1 = [start_vertex_1]
    cycle_2 = [start_vertex_2]
    pick_cycle_to_expand = 0
    while len(cycle_1) + len(cycle_2) < distance_matrix.shape[0]:

        if pick_cycle_to_expand % 2 == 0:
            cycle = cycle_1
        else:
            cycle = cycle_2

        closest_vertex = None
        closest_index = None
        closest_distance = np.inf

        for idx, current_vertex in enumerate(cycle):
            current_closest_vertex = find_closest_vertex(distance_matrix, current_vertex, cycle_1, cycle_2)
            if current_vertex+1 < distance_matrix.shape[0]:
                if distance_matrix[current_vertex, current_closest_vertex] \
                        + distance_matrix[current_closest_vertex, current_vertex+1] < closest_distance:
                    closest_vertex = current_closest_vertex
                    closest_index = idx
                    closest_distance = distance_matrix[current_vertex, current_closest_vertex] \
                        + distance_matrix[current_closest_vertex, current_vertex+1]
            else:
                if distance_matrix[current_vertex, current_closest_vertex] < closest_distance:
                    closest_vertex = current_closest_vertex
                    closest_index = idx
                    closest_distance = distance_matrix[current_vertex, current_closest_vertex]

        cycle.insert(closest_index+1, closest_vertex)
        pick_cycle_to_expand += 1

    return cycle_1, cycle_2


# coordinates_a = load_data_from_file('kroA100.tsp')
# distance_matrix_a = create_distance_matrix('kroA100.tsp')
# cycle_1, cycle_2 = nearest_neighbor_method(distance_matrix_a)
# print(cycle_1)
# print(cycle_2)
# # print(np.unique(np.concatenate([cycle_1, cycle_2]), return_counts=True))
# xs = [coord[0] for coord in coordinates_a]
# ys = [coord[1] for coord in coordinates_a]
# plot_results(xs, ys, cycle_1, cycle_2)
