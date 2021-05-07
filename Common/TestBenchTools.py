import numpy as np

def get_alg_results_struct(alg_fun_list):
    alg_names=[i.__name__ for i in alg_fun_list]
    alg_name_fun_list=zip(alg_names,alg_fun_list)
    algs_res=[Alg_results(i) for i in alg_name_fun_list]
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
    def __init__(self,name_fun,sp_no=1,methods_no=1):
        self.res=[[Alg_res_struct() for _ in range(sp_no)] for _ in range(methods_no) ]
        self.fun=name_fun[1]
        self.name=name_fun[0]
    def update_delta(self,delta,sp_no=0,method_no=0):
        res=self.res[method_no][sp_no]
        res.best_delta=delta if res.best_delta>delta else res.best_delta
    def update_time(self,time,sp_no=0,method_no=0):
        _time=self.res[method_no][sp_no]
        if time<_time.best_tm:_time.best_tm=time
        if time>_time.worst_tm:_time.worst_tm=time
        _time.sum_tm+=time
    def update_res(self,res,cycs,sp_no=0,method_no=0):
        _res=self.res[method_no][sp_no]
        if res<_res.best_res:
            _res.best_res=res
            _res.best_cycs=cycs
        if res>_res.worst_res:_res.worst_res=res
        _res.sum_res+=res
        _res.no_res+=1
    def show(self,sp_no=0,method_no=0):
        _res=self.res[method_no][sp_no]
        print(self.name,"method:",method_no,"starting_point:",sp_no,"avg_res: ",_res.sum_res/_res.no_res,"best: ", _res.best_res,\
                    "worst: ",_res.worst_res,"time:avg,best,worst:",_res.sum_tm/_res.no_res,\
                    _res.best_tm,_res.worst_tm,"best delta:",_res.best_delta)