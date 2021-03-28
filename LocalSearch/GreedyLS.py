
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

def chain_link_lenght(dist_m,mid,neighbours):
    return dist_m[mid,neighbours[0]]+dist_m[mid,neighbours[1]]
def is_neighbour(dist_m,vertecies,vtx):
    pass 
def get_neighbours(vtx,cyc):
    return (cyc[vtx-1],cyc[vtx+1])
def get_delta(dist_m,vertecies,move,cyc,cyc2=None):
    if cyc2==None:
        curr_distance=0
        new_distance=0
        neighbours=[]
        for vtx in vertecies:
            neighbours.append(get_neighbours(vtx,cyc))
        for idx,vtx in enumerate(vertecies):
            if move==VERTECIES:
                curr_distance+=chain_link_lenght(dist_m,vtx,neighbours[idx])
                new_distance+=chain_link_lenght(dist_m,vtx,neighbours[idx-1])
            else:
                curr_distance+=dist_m[vtx,neighbours[idx][PREV]]
                new_distance+=dist_m[vtx,neighbours[idx-1][PREV]]
    return new_distance-curr_distance
def try_to_improve(dist_m,cyc,cyc2=None):    
    move=EDGES if  rnd.getrandbits()  else VERTECIES
    improved=False
    if cyc2==None:
        for _ in range(2):
            for first_vtx in np.random.permutation(cyc):
                for sec_vtx in np.random.permutation(cyc):
                    delta=get_delta(dist_m,(first_vtx,sec_vtx),move,cyc)
                    if delta<0:
                        improved=True
                        cyc[first_vtx],cyc[sec_vtx]=cyc[sec_vtx],cyc[first_vtx]
                        break
                if improved: break
            move=not(move)
    return improved

def greedy_ls(cyc1,cyc2,dist_m,method=IN):
    imp_cyc1=np.copy(cyc1)
    imp_cyc2=np.copy(cyc2)
    if method==IN:
        improved=False
        while not(improved):
            curr_cyc=imp_cyc1 if  rnd.getrandbits() else imp_cyc2
            for _ in range(2):
                improved=try_to_improve(dist_m,curr_cyc)
                curr_cyc=imp_cyc1 if curr_cyc==imp_cyc2 else imp_cyc2
    return imp_cyc1, imp_cyc2

# %%
