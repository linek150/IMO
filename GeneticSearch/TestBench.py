from Common.CreateDistanceMatrix import create_distance_matrix
from Common.Helpers import get_total_distance
from Common.TestBenchTools import get_alg_results_struct, Alg_results,print_best
from .GeneticSearch import genetic_search



def get_results(instance_filename,no_iterations,iteration_time):

    algs=[genetic_search]
    algs_structs=get_alg_results_struct(algs)
    dist_m = create_distance_matrix(instance_filename)

    for _ in range(no_iterations):
        for alg in algs_structs:
            print(iteration_time)
            curr_res_cycs=alg.fun(dist_m,iteration_time)
            curr_res_lenght=get_total_distance(curr_res_cycs,dist_m)
            print(instance_filename,curr_res_lenght)
            alg.update_res(curr_res_lenght,curr_res_cycs)    
    return algs_structs
        

def run_test(no_iterations,iteration_time):
    print("in run test")
    algs_res_A=get_results("kroA200.tsp",no_iterations,iteration_time)
    algs_res_B=get_results("kroB200.tsp",no_iterations,iteration_time)
    print_best(algs_res_A,"kroA200.tsp")
    print_best(algs_res_B,"kroB200.tsp")
