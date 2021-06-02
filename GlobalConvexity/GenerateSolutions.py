import numpy as np
import pickle
from tqdm import tqdm

from Common.CreateDistanceMatrix import create_distance_matrix
from ImprovedLocalSearch.SteepestList import ls_steepest_list


def get_random_cycles(arr):
    np.random.shuffle(arr)
    cycle1 = arr[:len(arr)//2]
    cycle2 = arr[len(arr)//2:]
    return cycle1, cycle2


def get_cycle_length(cycle, distance_matrix):
    length = 0
    lengths = []
    for idx in range(len(cycle)):
        if idx - 1 < 0:
            length += distance_matrix[cycle[-1]][cycle[idx]]
            lengths.append(distance_matrix[cycle[-1]][cycle[idx]])
        else:
            length += distance_matrix[cycle[idx - 1]][cycle[idx]]
            lengths.append(distance_matrix[cycle[idx - 1]][cycle[idx]])
    return length


def generate_and_pickle(coordinates_file, num_solutions):
    distance_matrix = create_distance_matrix(coordinates_file)
    mean_length = 0
    for i in tqdm(range(num_solutions)):
        cycle_1, cycle_2 = get_random_cycles(np.arange(distance_matrix.shape[0]))
        cycle_1, cycle_2 = ls_steepest_list(cycle_1, cycle_2, distance_matrix)
        with open(f'solutions/{coordinates_file.strip("../Resources/").strip(".tsp")}/{i}.pkl', 'wb') as f:
            pickle.dump((cycle_1, cycle_2), f)
        mean_length += (get_cycle_length(cycle_1, distance_matrix) + get_cycle_length(cycle_2, distance_matrix))
    mean_length /= num_solutions
    print(mean_length)


generate_and_pickle('../Resources/kroA200.tsp', 1000)
generate_and_pickle('../Resources/kroB200.tsp', 1000)
