import pickle
from os import listdir
from os.path import join
from tqdm import tqdm

from Common.CreateDistanceMatrix import create_distance_matrix
from GlobalConvexity.Funcions import vertex_similarity, edges_similarity


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


def plot_solutions(solutions_path, distance_matrix):
    solutions = []
    files_paths = [join(solutions_path, f) for f in listdir(solutions_path)]
    for file_path in tqdm(files_paths):
        with (open(file_path, "rb")) as file:
            solution = pickle.load(file)
            solutions.append((solution, get_cycle_length(solution[0], distance_matrix) + get_cycle_length(solution[1], distance_matrix)))

    sorted_solutions = sorted(solutions, key=lambda x: x[1], reverse=False)

    lengths = []
    vertex_sims_all = []
    edge_sims_all = []
    vertex_sims_best = []
    edge_sims_best = []
    for solution in tqdm(sorted_solutions):
        lengths.append(solution[1])
        vertex_sims_best.append(vertex_similarity(solution[0], sorted_solutions[0][0]))
        edge_sims_best.append(edges_similarity(solution[0], sorted_solutions[0][0]))

        mean_vertex_sim = 0
        mean_edge_sim = 0
        for solution_2 in sorted_solutions:
            mean_vertex_sim += vertex_similarity(solution[0], solution_2[0])
            mean_edge_sim += edges_similarity(solution[0], solution_2[0])
        mean_vertex_sim /= len(sorted_solutions)
        mean_edge_sim /= len(sorted_solutions)
        vertex_sims_all.append(mean_vertex_sim)
        edge_sims_all.append(mean_edge_sim)

    with open(f'{solutions_path.strip("./solutions/")}.pkl', 'wb') as f:
        pickle.dump((lengths, vertex_sims_all, edge_sims_all, vertex_sims_best, edge_sims_best), f)


distance_matrix_a = create_distance_matrix('../Resources/kroA200.tsp')
distance_matrix_b = create_distance_matrix('../Resources/kroB200.tsp')
plot_solutions('./solutions/kroA200', distance_matrix_a)
plot_solutions('./solutions/kroB200', distance_matrix_b)


