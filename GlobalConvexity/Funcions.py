import numpy as np
from pkg_resources import VersionConflict
def vertex_similarity(solution_1,solution_2):
    pairs_comp=np.zeros((2,2),dtype=int)
    for idx1,cyc1 in enumerate(solution_1):
        for idx2,cyc2 in enumerate(solution_2):
            for vtx in cyc1:
                if vtx in cyc2:
                    pairs_comp[idx1][idx2]+=1
    #print("Indeksy: \n",pairs_comp)
    best_idx=np.argmax(pairs_comp)
    best_pair=(best_idx//len(solution_1),best_idx%len(solution_2))
    complement_pair=(best_pair[0]-1,best_pair[1]-1)
    return pairs_comp[best_pair]+pairs_comp[complement_pair]
def edges_similarity(solution_1,solution_2):
    pairs_comp=np.zeros((2,2),dtype=int)
    for idx1,cyc1 in enumerate(solution_1):
        for idx2,cyc2 in enumerate(solution_2):
            for cyc1_idx,vtx1 in enumerate(cyc1):
                edge1=(cyc1[cyc1_idx-1],vtx1)
                for cyc2_idx, vtx2 in enumerate(cyc2):
                    edge2=(cyc2[cyc2_idx-1],vtx2)
                    if edge1==edge2 or edge1==tuple(reversed(edge2)):
                        pairs_comp[idx1][idx2]+=1
    #print("Krawedzie: \n",pairs_comp)
    best_idx=np.argmax(pairs_comp)
    best_pair=(best_idx//len(solution_1),best_idx%len(solution_2))
    complement_pair=(best_pair[0]-1,best_pair[1]-1)
    return pairs_comp[best_pair]+pairs_comp[complement_pair]
