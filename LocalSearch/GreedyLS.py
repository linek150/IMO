
#%%
import numpy as np
import random as rnd
#method 0 - vertecies change
#method 1 - edges change
IN=0
OUT=1
EDGES=0
VERTECIES=1
PREV=0
NEXT=1

def chain_link_lenght(dist_m,mid,neighbours,cyc):
    to_prev=dist_m[cyc[mid],cyc[neighbours[PREV]]]
    to_next=dist_m[cyc[mid],cyc[neighbours[NEXT]]]
    return to_next+to_prev
def get_delta(dist_m,cyc_idxs,move,cyc,cyc2=None):
    if cyc2==None:
        curr_distance=0
        new_distance=0
        neighbours=[]
        for cyc_idx in cyc_idxs:
            neighbours.append((cyc_idx-1,(cyc_idx+1)%len(cyc)))
        if move==VERTECIES :
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
    return new_distance-curr_distance
def try_to_improve(dist_m,cyc,cyc2=None):    
    move=EDGES if  rnd.getrandbits(1)   else VERTECIES
    improved=False
    if cyc2==None:
        for _ in range(2):
            idxs=np.arange(len(cyc))
            np.random.shuffle(idxs)
            for i,first_idx in enumerate(idxs):
                improved=False
                for sec_idx in idxs[i+1:] if i+1<len(cyc) else []:
                    delta=get_delta(dist_m,(first_idx,sec_idx),move,cyc)
                    if delta<0:
                        improved=True
                        if move==VERTECIES:
                            cyc[first_idx],cyc[sec_idx]=cyc[sec_idx],cyc[first_idx]
                        else:
                            low_idx, hi_idx= (first_idx,sec_idx) if first_idx<sec_idx else (sec_idx,first_idx)
                            cyc=np.concatenate([cyc[:low_idx],np.flip(cyc[low_idx:hi_idx+1]),cyc[hi_idx+1:]])
                        break
                if improved: break
            if improved: break
            move=not(move)
    return delta,improved,cyc
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

def greedy_ls(cyc1,cyc2,dist_m,method=IN):
    imp_cycs=[np.copy(cyc1),np.copy(cyc2)]
    if method==IN:
        improved=True
        liczba_iteracji=0
        while improved:
            for idx,curr_cyc in enumerate(imp_cycs):
                delta,improved,imp_cycs[idx]=try_to_improve(dist_m,curr_cyc)
            liczba_iteracji+=1
        print(liczba_iteracji)
    return imp_cycs

# %%
