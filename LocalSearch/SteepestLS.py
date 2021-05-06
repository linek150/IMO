
#%%
import numpy as np
import random as rnd
#method 0 - vertecies change
#method 1 - edges change
VERTECIES=0
EDGES=1
PREV=0
NEXT=1
IN=0
OUT=1

def chain_link_lenght(dist_m,mid,neighbours,cyc):
    to_prev=dist_m[cyc[mid],cyc[neighbours[PREV]]]
    to_next=dist_m[cyc[mid],cyc[neighbours[NEXT]]]
    return to_next+to_prev
def make_improvement(dist_m,first_idx,sec_idx,cyc,cyc2=None):
    if cyc2 is None:
        low_idx, hi_idx= (first_idx,sec_idx) if first_idx<sec_idx else (sec_idx,first_idx)
        cyc=np.concatenate([cyc[:low_idx],np.flip(cyc[low_idx:hi_idx+1]),cyc[hi_idx+1:]])
        return cyc
    else:
        pass
    return cyc,cyc2

def get_delta(dist_m,cyc_idxs,cyc,cyc2=None):
    curr_distance=-1
    new_distance=-1
    if cyc2 is None:
        if cyc_idxs==(len(cyc)-1,0) or cyc_idxs==(0,len(cyc)-1): return 0
        low_idx=cyc_idxs[0] if cyc_idxs[0]<cyc_idxs[1] else cyc_idxs[1]
        hi_idx=cyc_idxs[0] if cyc_idxs[0]>cyc_idxs[1] else cyc_idxs[1]
        curr_distance=dist_m[cyc[low_idx],cyc[low_idx-1]]+dist_m[cyc[hi_idx],cyc[(hi_idx+1)%len(cyc)]]
        new_distance=dist_m[cyc[low_idx-1],cyc[hi_idx]]+dist_m[cyc[low_idx],cyc[(hi_idx+1)%len(cyc)]]
    else:
        curr_d_1=dist_m[cyc[cyc_idxs[0]],cyc[cyc_idxs[0]-1]]+dist_m[cyc[cyc_idxs[0]],cyc[(cyc_idxs[0]+1)%len(cyc)]]
        curr_d_2=dist_m[cyc2[cyc_idxs[1]],cyc2[cyc_idxs[1]-1]]+dist_m[cyc2[cyc_idxs[1]],cyc2[(cyc_idxs[1]+1)%len(cyc)]]
        curr_distance=curr_d_1+curr_d_2
        new_d_1=dist_m[cyc2[cyc_idxs[1]],cyc[cyc_idxs[0]-1]]+dist_m[cyc2[cyc_idxs[1]],cyc[(cyc_idxs[0]+1)%len(cyc)]]
        new_d_2=dist_m[cyc[cyc_idxs[0]],cyc2[cyc_idxs[1]-1]]+dist_m[cyc[cyc_idxs[0]],cyc2[(cyc_idxs[1]+1)%len(cyc)]]
        new_distance=new_d_1+new_d_2
    return new_distance-curr_distance
def try_to_improve(cyc1,cyc2,dist_m):   
    improved=False
    best_delta=0
    best_method=-1
    delta=0
    idxs=np.arange(len(cyc1))
    cycs=[cyc1,cyc2]
    #try to improve both cycle
    for curr_cyc in range(len(cycs)):
        for first_idx in idxs:
            for sec_idx in idxs[first_idx+1:] if first_idx+1<len(cycs[curr_cyc]) else []:
                delta=get_delta(dist_m,(first_idx,sec_idx),cycs[curr_cyc])
                if delta<best_delta:
                   # cycs[curr_cyc]=make_improvement(dist_m,first_idx,sec_idx,cycs[curr_cyc])
                    #cyc1,cyc2=cycs
                    best_method=IN
                    best_delta=delta
                    best_first=first_idx
                    best_sec=sec_idx
                    best_cyc_idx=curr_cyc

    idxs2=np.copy(idxs)
    for first_idx in idxs:
        for sec_idx in idxs2:
            delta=get_delta(dist_m,(first_idx,sec_idx),cyc1,cyc2)
            if delta<best_delta:
                best_method=OUT
                best_delta=delta
                best_first=first_idx
                best_sec=sec_idx
                #cyc1[first_idx],cyc2[sec_idx]=cyc2[sec_idx],cyc1[first_idx]
    if best_delta<0:

        improved=True
        if best_method==IN:
            cycs[best_cyc_idx]=make_improvement(dist_m,best_first,best_sec,cycs[best_cyc_idx])
            cyc1,cyc2=cycs
        elif best_method==OUT:
            cyc1[best_first],cyc2[best_sec]=cyc2[best_sec],cyc1[best_first]
    return best_delta,improved,cyc1,cyc2   

def ls_steepest(cyc1,cyc2,dist_m):
    imp_cycs=[np.copy(cyc1),np.copy(cyc2)]
    improved=True
    while improved:
        _,improved,imp_cycs[0],imp_cycs[1]=try_to_improve(imp_cycs[0],imp_cycs[1],dist_m)
        
    return imp_cycs[0],imp_cycs[1]

