from ..ImprovedLocalSearch.SteepestList import ls_steepest_list as ls
from ..Common.Helpers import get_random_cycles,get_total_distance

def random_start_ls(dist_m):
    vertecies_arr=list(range(len(dist_m[0])))
    cycs=get_random_cycles(vertecies_arr)
    imp_cycs=ls(cycs[0],cycs[1],dist_m)
    return imp_cycs

def ls_multi_start(dist_m,iter_no=1):
    best_cycs=None
    best_length=float('inf')
    for i in range(iter_no):
        cycs=random_start_ls(dist_m)
        if get_total_distance(cycs, dist_m)<best_length:
            best_cycs=cycs
    assert best_cycs!=None
    return best_cycs