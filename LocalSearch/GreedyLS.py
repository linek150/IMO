
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
def make_improvement(dist_m,first_idx,sec_idx,method,cyc,cyc2=None):
    if cyc2 is None:
        if method==VERTECIES:
            cyc[first_idx],cyc[sec_idx]=cyc[sec_idx],cyc[first_idx]
        else:
            low_idx, hi_idx= (first_idx,sec_idx) if first_idx<sec_idx else (sec_idx,first_idx)
            cyc=np.concatenate([cyc[:low_idx],np.flip(cyc[low_idx:hi_idx+1]),cyc[hi_idx+1:]])
        return cyc
    else:
        pass
    return cyc,cyc2

def get_delta(dist_m,cyc_idxs,method,cyc,cyc2=None):
    if cyc2 is None:
        curr_distance=0
        new_distance=0
        neighbours=[]
        for cyc_idx in cyc_idxs:
            neighbours.append((cyc_idx-1,(cyc_idx+1)%len(cyc)))
        if method==VERTECIES :
            for curr_idx,cyc_idx in enumerate(cyc_idxs):
                curr_distance+=chain_link_lenght(dist_m,cyc_idx,neighbours[curr_idx],cyc)
                new_distance+=chain_link_lenght(dist_m,cyc_idx,neighbours[curr_idx-1],cyc)
            if abs(cyc_idxs[0]-cyc_idxs[1])==1 or cyc_idxs==(len(cyc)-1,0) or cyc_idxs==(0,len(cyc)-1):
                new_distance+=2*dist_m[cyc[cyc_idxs[0]],cyc[cyc_idxs[1]]]
        else:
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
def try_to_improve(cyc1,cyc2,dist_m,method):   
    improved=False
    delta=0
    idxs=np.arange(len(cyc1))
    move=IN if  rnd.getrandbits(1)  else OUT
    #try inside of every cycle and between cycles
    for _ in range(2):
        if move==IN:#exchange in cycle
            np.random.shuffle(idxs)
            cycs=[cyc1,cyc2]
            curr_cyc=rnd.getrandbits(1)
            #try to improve both cycle
            for _ in range(len(cycs)):
                for i,first_idx in enumerate(idxs):
                    for sec_idx in idxs[i+1:] if i+1<len(cycs[curr_cyc]) else []:
                        delta=get_delta(dist_m,(first_idx,sec_idx),method,cycs[curr_cyc])
                        if delta<0:
                            improved=True
                            cycs[curr_cyc]=make_improvement(dist_m,first_idx,sec_idx,method,cycs[curr_cyc])
                            cyc1,cyc2=cycs
                            break
                    if improved: break
                if improved: break
                curr_cyc=(curr_cyc+1)%len(cycs)
        else:#exchange between cycles
            np.random.shuffle(idxs)
            idxs2=np.copy(idxs)
            np.random.shuffle(idxs2)
            for first_idx in idxs:
                for sec_idx in idxs2:
                    delta=get_delta(dist_m,(first_idx,sec_idx),None,cyc1,cyc2)
                    if delta<0:
                        improved=True
                        cyc1[first_idx],cyc2[sec_idx]=cyc2[sec_idx],cyc1[first_idx]
                        break
                if improved:break
        if improved: break
        move=(move+1)%2
    return delta,improved,cyc1,cyc2   
def cycle_length(cycle, distance_matrix):
    length = 0
    lengths = []
    for idx in range(len(cycle)):
        if idx - 1 < 0:
            length += distance_matrix[cycle[-1]][cycle[idx]]
            lengths.append(distance_matrix[cycle[-1]][cycle[idx]])
        else:
            length += distance_matrix[cycle[idx-1]][cycle[idx]]
            lengths.append(distance_matrix[cycle[idx-1]][cycle[idx]])
    return length

def greedy_ls(cyc1,cyc2,dist_m,method=VERTECIES):
    imp_cycs=[np.copy(cyc1),np.copy(cyc2)]
    improved=True
    while improved:
        _,improved,imp_cycs[0],imp_cycs[1]=try_to_improve(imp_cycs[0],imp_cycs[1],dist_m,method)
    return imp_cycs[0],imp_cycs[1]

# %%
