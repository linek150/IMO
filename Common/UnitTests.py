from .CreateDistanceMatrix import load_data_from_file,create_distance_matrix,get_coordinates
from .Visualize import plot_results
from .Helpers import get_random_cycles,get_total_distance
import time

def random_start(algorithm_fun,instance_filename):
    dist_m = create_distance_matrix(instance_filename)
    vertecis_arr=list(range(len(dist_m[0])))
    random_cycles=get_random_cycles(vertecis_arr)
    xs,ys=get_coordinates(instance_filename)
    length_before=get_total_distance(random_cycles, dist_m)
    #plot_results(xs,ys,random_cycles[0],random_cycles[1],"Before")
    start=time.time()
    improved_cycs=algorithm_fun(*random_cycles,dist_m)
    stop=time.time()
    length_after=get_total_distance(improved_cycs, dist_m)
    plot_results(xs, ys, improved_cycs[0], improved_cycs[1],"After alg")
    print(algorithm_fun.__name__," Final result: ",length_after, "Time:",stop-start,"[s]")