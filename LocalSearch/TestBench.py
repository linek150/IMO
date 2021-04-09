from ..Heuristics.GreedyCycle import greedy_cycle
from ..Common.CreateDistanceMatrix import load_data_from_file,create_distance_matrix
from ..Common.Visualize import plot_results
from ..Heuristics.GreedyCycle import greedy_cycle
from .SteepestLS import steepest_local_search
from .RandomWalk import random_local_search
from .GreedyLS import greedy_ls
import numpy as np
import time as t
VERTECIES=0
EDGES=1
WORST=0
BEST=1
AVG=2
TIME=3
CYCLES=4
GLS="greedyLS"
SLS="steepestLS"
RW="randomWalk"
def get_total_distance(cycles,distance_matrix):
    total_distance=0
    for cycle in cycles:
        for i in range(len(cycle)):
            total_distance+=distance_matrix[cycle[i-1],cycle[i]]
    return total_distance
class Alg_res_struct:
    def __init__(self):
        self.worst_res=-np.inf
        self.best_res=np.inf
        self.sum_res=0
        self.best_tm=np.inf
        self.worst_tm=-np.inf
        self.sum_tm=0
        self.best_cycs=None
        self.no_res=0
        self.best_delta=0
class Alg_results:
    def __init__(self,alg,alg_name,sp_no=1,methods_no=1):
        self.res=[[Alg_res_struct() for _ in range(sp_no)] for _ in range(methods_no) ]
        #self.res=[[Alg_res_struct()]*sp_no]*methods_no
        self.fun=alg
        self.name=alg_name
    def update_delta(self,delta,sp_no=1,method_no=1):
        res=self.res[method_no][sp_no]
        res.best_delta=delta if res.best_delta>delta else res.best_delta
    def update_time(self,time,sp_no=1,method_no=1):
        _time=self.res[method_no][sp_no]
        if time<_time.best_tm:_time.best_tm=time
        if time>_time.worst_tm:_time.worst_tm=time
        _time.sum_tm+=time
    def update_res(self,res,cycs,sp_no=1,method_no=1):
        _res=self.res[method_no][sp_no]
        if res<_res.best_res:
            _res.best_res=res
            _res.best_cycs=cycs
        if res>_res.worst_res:_res.worst_res=res
        _res.sum_res+=res
        _res.no_res+=1
    def show(self,sp_no=1,method_no=1):
        _res=self.res[method_no][sp_no]
        print(self.name,"method:",method_no,"starting_point:",sp_no,"avg_res: ",_res.sum_res/_res.no_res,"best: ", _res.best_res,\
                    "worst: ",_res.worst_res,"time:avg,best,worst:",_res.sum_tm/_res.no_res,\
                    _res.best_tm,_res.worst_tm,"best delta:",_res.best_delta)

def get_random_cycles(arr,n=2):
    np.random.shuffle(arr)
    cycle1=arr[:len(arr)//2]
    cycle2=arr[len(arr)//2:]
    return (cycle1,cycle2)
def get_results(instance_filename):
    dist_m = create_distance_matrix(instance_filename)
    vertecis_arr=list(range(len(dist_m[0])))
    #crete structures for all algorithm
    algs=[greedy_ls,steepest_local_search,random_local_search]
    #worst,best,avrg,best_cycles
    algs_res=[Alg_results(algs[i],name,2,2) for i,name in enumerate([GLS,SLS,RW])]
    for start_vertex in range(2):#range(len(dist_m[0])):
        random_cycles=get_random_cycles(vertecis_arr)
        greedy_cycles=(greedy_cycle(dist_m,start_vertex))
        start_cycs=[random_cycles,greedy_cycles]
        #3 algorithms
        for idx,alg_res in enumerate(algs_res):
            for sp_no,cycs in enumerate(start_cycs):    
                for meth_no,method in enumerate([VERTECIES,EDGES]):
                    length_before=get_total_distance(cycs,dist_m)
                    time=t.time()
                    curr_res_cycs=algs[idx](cycs[0],cycs[1],dist_m,method)
                    time=t.time()-time
                    curr_res_lenght=get_total_distance(curr_res_cycs,dist_m)
                    length_delta=curr_res_lenght-length_before

                    alg_res.update_delta(length_delta,sp_no,meth_no)
                    alg_res.update_time(time,sp_no,meth_no)
                    alg_res.update_res(curr_res_lenght,curr_res_cycs,sp_no,meth_no)
    return algs_res
        
def print_best(algs_res,file_name):
    coordinates=load_data_from_file(file_name)
    xs = [coord[0] for coord in coordinates]
    ys = [coord[1] for coord in coordinates]
    print(file_name,": ")
    for alg in algs_res:
        for method_no,method in enumerate(alg.res):
            for sp_no,sp in enumerate(method):
                plot_results(xs,ys,sp.best_cycs[0],sp.best_cycs[1],alg.name+" method_no: "+str(method_no)+" start_point_no: "+str(sp_no))
                alg.show(sp_no,method_no)
def run_test():
    
    algs_res_A=get_results("kroA100.tsp")
    print_best(algs_res_A,"kroA100.tsp")
    algs_res_B=get_results("kroB100.tsp")
    print_best(algs_res_B,"kroB100.tsp")
                

#method_dict_x method:[best_distance,worst_distance,avg_distamce,best_cycles]



