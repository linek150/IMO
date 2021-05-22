import itertools
import time
from operator import attrgetter
import copy

import numpy as np

from Common.CreateDistanceMatrix import load_data_from_file, create_distance_matrix
from Common.Visualize import plot_results
from .Individual import Individual
from ImprovedLocalSearch.SteepestList import ls_steepest_list


class GeneticSearch:

    def __init__(self, distance_matrix, runtime=5, elite_population=20):
        self.distance_matrix = distance_matrix
        self.runtime = runtime
        self.elite_population = elite_population
        self.population_list = self.generate_population()

    def get_random_cycles(self):
        vertices = np.arange(self.distance_matrix.shape[0])
        np.random.shuffle(vertices)
        cycle_1 = vertices[:len(vertices) // 2]
        cycle_2 = vertices[len(vertices) // 2:]
        return cycle_1, cycle_2

    def get_cycle_length(self, cycle):
        length = 0
        lengths = []
        for idx in range(len(cycle)):
            if idx - 1 < 0:
                length += self.distance_matrix[cycle[-1]][cycle[idx]]
                lengths.append(self.distance_matrix[cycle[-1]][cycle[idx]])
            else:
                length += self.distance_matrix[cycle[idx - 1]][cycle[idx]]
                lengths.append(self.distance_matrix[cycle[idx - 1]][cycle[idx]])
        return length

    def calculate_fitness(self, cycle_1, cycle_2):
        # We want larger fitness to be better so -1*fitness
        fitness = -1 * (self.get_cycle_length(cycle_1) + self.get_cycle_length(cycle_2))
        return fitness

    def generate_population(self):
        initial_population = []
        for i in range(self.elite_population):
            cycle_1, cycle_2 = self.get_random_cycles()
            cycle_1, cycle_2 = ls_steepest_list(cycle_1, cycle_2, self.distance_matrix)
            fitness = self.calculate_fitness(cycle_1, cycle_2)
            individual = Individual(cycle_1, cycle_2, fitness)
            if individual not in initial_population:
                initial_population.append(individual)
        return initial_population

    def pair_grouper(self, iterable, n, fillvalue=None):
        "Collect data into fixed-length chunks or blocks"
        # Taken from itertools recipes:
        # https://docs.python.org/2/library/itertools.html#recipes
        # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
        args = [iter(iterable)] * n
        return itertools.zip_longest(fillvalue=fillvalue, *args)

    def recombination(self, individual_1, individual_2):
        child=copy.copy(individual_1)
        for cycle in child.cycles:
            edges_to_rm=[]
            for vtx_idx,vtx in enumerate(cycle):
                curr_abs_edge=(cycle[vtx_idx-1],vtx)
                if not(GeneticSearch.occur_in_individual(curr_abs_edge,individual_2)):
                    curr_idx_edge=(vtx_idx-1 if vtx_idx-1 >=0 else len(cycle)-1 ,vtx_idx)
                    edges_to_rm.append(curr_idx_edge)
            GeneticSearch.remove_edges_from_cyc(edges_to_rm,cycle)
        child.recreate_cycles(self.distance_matrix)
        return child

    @staticmethod
    def remove_edges_from_cyc(edges,cycle):
        prev_edge=edges[0]
        cyc_copy=[]
        for edge in edges[1:]:
            if prev_edge[1]!=edge[0]:
                cyc_copy.append(cycle[edge[0]])  
            prev_edge=edge
        for idx,elem in enumerate(cyc_copy):
            cycle[idx]=elem
        while len(cyc_copy)<len(cycle):
            cycle.pop()

    @staticmethod
    def occur_in_individual(edge,individual):
        for cycle in individual.cycles:
            for vtx_idx,vtx in enumerate(cycle):
                curr_edge=(cycle[vtx_idx-1],vtx)
                if curr_edge==edge or curr_edge==tuple(reversed(edge)):
                    return True
        return False

    def search(self, perform_ls):
        start_time = time.time()
        while time.time() - start_time < self.runtime:
            np.random.shuffle(self.population_list)
            all_individuals_pairs = [pair for pair in self.pair_grouper(self.population_list, 2)]
            for parent_1, parent_2 in all_individuals_pairs:
                child = self.recombination(parent_1, parent_2)
                if perform_ls:
                    child.cycle_1, child.cycle_2 = ls_steepest_list(child.cycle_1, child.cycle_2, self.distance_matrix)
                child.fitness = self.calculate_fitness(child.cycle_1, child.cycle_2)
                if child not in self.population_list:
                    self.population_list.append(child)
            population_list_sorted = sorted(self.population_list, key=lambda x: x.fitness, reverse=True)
            best_individuals = population_list_sorted[:self.elite_population]
            self.population_list = best_individuals
        best = max(self.population_list, key=attrgetter('fitness'))
        return best.cycle_1, best.cycle_2


def genetic_search(distance_matrix, runtime=5, perform_ls=True):
    gen_search_obj = GeneticSearch(distance_matrix, runtime)
    return gen_search_obj.search(perform_ls)


# coordinates_a = load_data_from_file('../Heuristics/kroA100.tsp')
# distance_matrix_a = create_distance_matrix('../Heuristics/kroA100.tsp')
# gs = GeneticSearch(distance_matrix_a)
# best_result = gs.search()
# xs = [coord[0] for coord in coordinates_a]
# ys = [coord[1] for coord in coordinates_a]
# plot_results(xs, ys, best_result.cycle_1, best_result.cycle_2)
# print(-1*best_result.fitness)
