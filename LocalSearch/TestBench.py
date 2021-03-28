from ..Heuristics.GreedyCycle import greedy_cycle
from ..Common.CreateDistanceMatrix import load_data_from_file,create_distance_matrix
from ..Common.Visualize import plot_results
from ..Heuristics.NearestNeighbor import nearest_neighbor_method
from .SteepestLS import steepest_local_search
def run_test():
    coordinates_a = load_data_from_file('kroA100.tsp')
    distance_matrix_a = create_distance_matrix('kroA100.tsp')
    cycle_1, cycle_2 = nearest_neighbor_method(distance_matrix_a)
    xs = [coord[0] for coord in coordinates_a]
    ys = [coord[1] for coord in coordinates_a]
    plot_results(xs, ys, cycle_1, cycle_2)
    cycle_1_improved, cycle_2_improved = steepest_local_search(cycle_1, cycle_2, distance_matrix_a, method=0)
    plot_results(xs, ys, cycle_1_improved, cycle_2_improved)