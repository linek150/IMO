
from itertools import cycle
from ..ExtendedLocalSearch.ILS1 import ils1_method
from ExtendedLocalSearch.GreedyCycleForILS2 import greedy_cycle_for_ils2
import numpy as np
class Individual:
    def __init__(self, cycle_1, cycle_2, fitness):
        self.cycle_1 = cycle_1
        self.cycle_2 = cycle_2
        self.fitness = fitness

        self.cycles=[self.cycle_1,self.cycle_2]
    def recreate_cycles(self,dist_m):
        greedy_cycle_for_ils2(self.cycle_1,self.cycle_2,dist_m)
        #if np.random.rand()<0.1:
           # self.cycle_1,self.cycle_2=ils1_method(self.cycle_1,self.cycle_2,dist_m)
        self.cycle_1=np.array(self.cycle_1)
        self.cycle_2=np.array(self.cycle_2)
        self.cycles=[self.cycle_1,self.cycle_2]
        
    def __eq__(self, other):
        return self.fitness == other.fitness
    def __copy__(self):
        return Individual(list(self.cycle_1),list(self.cycle_2),self.fitness.copy())
