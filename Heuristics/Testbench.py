import Visualize as vis
import CreateDistanceMatrix as cdm
import NearestNeighbor as nn
import GreedyCycle as gc
import numpy as np

coordinates_a = cdm.load_data_from_file('kroA100.tsp')
distance_matrix_a = cdm.create_distance_matrix('kroA100.tsp')
gc_1, gc_2 = gc.greedy_cycle(distance_matrix_a)
nn_1, nn_2 = nn.nearest_neighbor_method(distance_matrix_a)
#print(cycle_1)
#print(cycle_2)
xs = [coord[0] for coord in coordinates_a]
ys = [coord[1] for coord in coordinates_a]
vis.plot_results(xs, ys, nn_1, nn_2)
vis.plot_results(xs,ys,gc_1,gc_2)