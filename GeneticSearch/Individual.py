
class Individual:
    def __init__(self, cycle_1, cycle_2, fitness):
        self.cycle_1 = cycle_1
        self.cycle_2 = cycle_2
        self.fitness = fitness

    def __eq__(self, other):
        return self.fitness == other.fitness
