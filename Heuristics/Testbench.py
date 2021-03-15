import Visualize as vis
import CreateDistanceMatrix as cdm
import NearestNeighbor as nn
import GreedyCycle as gc
import RegretCycle as rc
import numpy as np
import random 
import copy 
GC="greedy_cycle"
RC="regret_cycle"
NN="nearest_neighbor"
BEST=0
WORST=1
AVG=2
CYCLES=3
def get_total_distance(cycle,distance_matrix):
    total_distance=0
    for i in range(len(cycle)):
        total_distance+=distance_matrix[cycle[i-1],cycle[i]]
    return total_distance
def get_results(instance_filename):
    coordinates_a = cdm.load_data_from_file(instance_filename)
    distance_matrix = cdm.create_distance_matrix(instance_filename)
    #method_dict [best_distance,worst_distance,avg_distamce,best_cycles]
    method_dict={i:[np.inf,-np.inf,0,[]] for i in [GC,RC,NN]}
    for start_vertex in range(len(distance_matrix[0])):
        #run every method with start_vertex
        method_dict.get(GC).append(gc.greedy_cycle(distance_matrix,start_vertex))
        method_dict.get(RC).append(rc.greedy_cycle(distance_matrix,start_vertex))
        distance_matrix_cp=copy.deepcopy(distance_matrix)
        method_dict.get(NN).append(nn.nearest_neighbor_method(distance_matrix_cp,start_vertex))
        #save results
        for key,method in method_dict.items():
            total_distance=0
            #calculate total distance for given method and start_vertex
            for cycle in method[-1]:
                cycle_distance=get_total_distance(cycle,distance_matrix)
                total_distance=total_distance+cycle_distance
            method[AVG]+=total_distance
            if total_distance>method[WORST]:
                method[WORST]=total_distance
            if total_distance<method[BEST]:
                method.pop(CYCLES)
                method[BEST]=total_distance
                continue
            #remove iteration cycle
            method.pop()
    for key,method in method_dict.items():
        method[AVG]=method[AVG]/len(distance_matrix[0])
    return method_dict
def print_best(method_dict,file_name):
    coordinates=cdm.load_data_from_file(file_name)
    xs = [coord[0] for coord in coordinates]
    ys = [coord[1] for coord in coordinates]
    print(file_name,": ")
    for key,method in method_dict.items():
        vis.plot_results(xs,ys,method[CYCLES][0],method[CYCLES][1])
        print(key,"avg: ",method[AVG],"best: ", method[BEST],"worst: ",method[WORST])

#method_dict_x method:[best_distance,worst_distance,avg_distamce,best_cycles]



method_dict_a=get_results("kroA100.tsp")
print_best(method_dict_a,"kroA100.tsp")
method_dict_b=get_results("kroB100.tsp")
print_best(method_dict_b,"kroB100.tsp")
