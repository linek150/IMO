import numpy as np
from scipy.spatial import distance_matrix
import pathlib as path
_resources="/Resources/"

def load_data_from_file(filename):
    with open(str(path.Path(__file__).parents[1])+_resources+filename, 'r') as f:
        data = [x.strip() for x in f.readlines()][6:-1]
    data_coordinates = [[int(coordinates.split()[1]), int(coordinates.split()[2])] for coordinates in data]
    return data_coordinates


def create_distance_matrix(filename):
    data_coordinates = load_data_from_file(filename)
    dist_matrix = np.round(distance_matrix(data_coordinates, data_coordinates), 0)
    return dist_matrix


# kroa = create_distance_matrix('kroA100.tsp')
# krob = create_distance_matrix('kroB100.tsp')
# print(kroa.shape)
# print(kroa)
# print(krob.shape)
# print(krob)
# # To check that distance was calculated correctly
# print(np.round(np.sqrt((2848-1380)**2+(96-939)**2), 0))
