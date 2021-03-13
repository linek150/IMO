import numpy as np

    

def greedy_cycle(distance_matrix):
    unused_vertex=list(range(distance_matrix.shape[0]))
    start_vertex_1=np.random.choice(distance_matrix.shape[0])
    start_vertex_2=np.argmax(distance_matrix[start_vertex_1])
    cycle1=[start_vertex_1]
    unused_vertex.remove(start_vertex_1)
    cycle2=[start_vertex_2]
    unused_vertex.remove(start_vertex_2) 
    cycle1.append(unused_vertex[np.argmin(distance_matrix[start_vertex_1,unused_vertex])])
    unused_vertex.remove(cycle1[-1])
    cycle2.append(unused_vertex[np.argmin(distance_matrix[start_vertex_2,unused_vertex])])
    unused_vertex.remove(cycle2[-1])
    
    which_cycle=0
    while unused_vertex != []:
        cycle=cycle1 if which_cycle%2==0 else cycle2
        smallest_lenght_increase=np.inf
        best_insert_idx=-1
        best_vertex=-1
        for split_idx in range(len(cycle)):
            curr_distance=distance_matrix[cycle[split_idx-1],cycle[split_idx]]
            for vertex in unused_vertex:
                distance1=distance_matrix[vertex,cycle[split_idx]]
                distance2=distance_matrix[vertex,cycle[split_idx-1]]
                new_distance=distance1+distance2
                if new_distance - curr_distance < smallest_lenght_increase:
                    smallest_lenght_increase = new_distance - curr_distance
                    best_insert_idx=split_idx
                    best_vertex=vertex
        cycle.insert(best_insert_idx,best_vertex)
        unused_vertex.remove(best_vertex)
        which_cycle+=1
    return cycle1, cycle2

    

    
