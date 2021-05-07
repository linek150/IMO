from Common.CreateDistanceMatrix import load_data_from_file, create_distance_matrix
from Common.Visualize import plot_results
from Common.Helpers import get_total_distance, get_random_cycles
from Common.TestBenchTools import get_alg_results_struct, Alg_results,print_best
from .ILS1 import ils1_method
from .ILS2 import ils2_method
from .MSLS import ls_multi_start

import numpy as np
import time as t

NO_ITERATIONS=2
NO_STARTS_MSLS=2
def get_results(instance_filename):
    algs=[ls_multi_start,ils1_method,ils2_method]
    algs_structs=get_alg_results_struct(algs)
    dist_m = create_distance_matrix(instance_filename)
    
    vertecies_arr=list(range(len(dist_m[0])))

    for _ in range(NO_ITERATIONS):
        rand_cycs=get_random_cycles(vertecies_arr)
        for alg in algs_structs:
            if alg.fun is ls_multi_start:
                time=t.time()
                curr_res_cycs=alg.fun(dist_m,NO_STARTS_MSLS)
                time=t.time()-time
            else:
                curr_res_cycs=alg.fun(rand_cycs[0],rand_cycs[1],dist_m,time)
            curr_res_lenght=get_total_distance(curr_res_cycs,dist_m)
            alg.update_time(time)
            alg.update_res(curr_res_lenght,curr_res_cycs)    
    return algs_structs
        

def run_test():
    algs_res_A=get_results("kroA200.tsp")
    algs_res_B=get_results("kroB200.tsp")
    print_best(algs_res_A,"kroA200.tsp")
    print_best(algs_res_B,"kroB200.tsp")