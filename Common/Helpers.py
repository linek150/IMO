import numpy as np
def get_total_distance(cycles,distance_matrix):
    total_distance=0
    for cycle in cycles:
        for i in range(len(cycle)):
            total_distance+=distance_matrix[cycle[i-1],cycle[i]]
    return total_distance


def get_random_cycles(arr,n=2):
    np.random.shuffle(arr)
    cycle1=arr[:len(arr)//2]
    cycle2=arr[len(arr)//2:]
    return (cycle1,cycle2)