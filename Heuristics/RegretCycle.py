import numpy as np
BEST=0
SECOND_BEST=1
SPLIT_IDX=2


def greedy_cycle(distance_matrix):
    unused_vertex=list(range(distance_matrix.shape[0]))
    
    start_vertex_1=np.random.choice(distance_matrix.shape[0])
    cycle1=[start_vertex_1]
    unused_vertex.remove(start_vertex_1)
    start_vertex_2=np.argmax(distance_matrix[start_vertex_1,[unused_vertex]])
    cycle2=[start_vertex_2]
    unused_vertex.remove(start_vertex_2) 
    cycle1.append(unused_vertex[np.argmin(distance_matrix[start_vertex_1,unused_vertex])])
    unused_vertex.remove(cycle1[-1])
    cycle2.append(unused_vertex[np.argmin(distance_matrix[start_vertex_2,unused_vertex])])
    unused_vertex.remove(cycle2[-1])
    
    which_cycle=0
    while unused_vertex != []:
        best_cost=[[i,i,0] for i in [np.inf]*len(unused_vertex)]
        vertex_dict=dict(zip(unused_vertex,best_cost))
        
       
        cycle=cycle1 if which_cycle%2==0 else cycle2
        
        #find best first step
        for split_idx in range(len(cycle)):
            curr_distance=distance_matrix[cycle[split_idx-1],cycle[split_idx]]
            for vertex in unused_vertex:
                distance1=distance_matrix[vertex,cycle[split_idx]]
                distance2=distance_matrix[vertex,cycle[split_idx-1]]
                new_distance=distance1+distance2
                curr_delta = new_distance - curr_distance
                # update best result
                if curr_delta < vertex_dict.get(vertex)[SECOND_BEST]:
                    if curr_delta < vertex_dict.get(vertex)[BEST]:
                        vertex_dict.get(vertex)[SECOND_BEST]=vertex_dict.get(vertex)[BEST]
                        vertex_dict.get(vertex)[BEST]= curr_delta
                        vertex_dict.get(vertex)[SPLIT_IDX]=split_idx
                        continue
                    vertex_dict.get(vertex)[SECOND_BEST]=curr_delta
        highest_regret_vertex=0
        highest_regret = -np.inf
        for vertex in unused_vertex:
            curr_regret=vertex_dict.get(vertex)[SECOND_BEST]-vertex_dict.get(vertex)[BEST]
            if curr_regret>highest_regret:
                highest_regret=curr_regret
                highest_regret_vertex=vertex
        #add vertex with highest regret to cycle
        cycle.insert(vertex_dict.get(highest_regret_vertex)[SPLIT_IDX],highest_regret_vertex)
        unused_vertex.remove(highest_regret_vertex)
        which_cycle+=1

    return cycle1, cycle2