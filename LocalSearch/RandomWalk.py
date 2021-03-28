import numpy as np
# from Heuristics.CreateDistanceMatrix import *
# from Heuristics.Visualize import plot_results


def random_walk_method(distance_matrix):
    permuted_vertices = np.random.permutation(distance_matrix.shape[0])
    if distance_matrix.shape[0] % 2 == 0:
        cycle_1 = permuted_vertices[:int(permuted_vertices.shape[0]/2)]
        cycle_2 = permuted_vertices[int(permuted_vertices.shape[0]/2):]
    else:
        cycle_1 = permuted_vertices[:int((permuted_vertices.shape[0]+1)/2)]
        cycle_2 = permuted_vertices[int((permuted_vertices.shape[0]+1)/2):]
    return cycle_1, cycle_2


# coordinates_a = load_data_from_file('../Heuristics/kroA100.tsp')
# distance_matrix_a = create_distance_matrix('../Heuristics/kroA100.tsp')
# xs = [coord[0] for coord in coordinates_a]
# ys = [coord[1] for coord in coordinates_a]
# cycle_1, cycle_2 = random_walk_method(distance_matrix_a)
# plot_results(xs, ys, cycle_1, cycle_2)
