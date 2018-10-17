from modules.crossover import onepoint, uniform


class CrossoverFacade:
    ONE_POINT = 1
    UNIFORM = 2

    def __init__(self):
        self._crossover = [
            'one_point',
            'uniform',
        ]

    def select_department(self, crossover_name):
        if crossover_name is self._crossover[0]:
            return onepoint.OnePointCrossover(self.ONE_POINT)
        elif crossover_name is self._crossover[1]:
            return uniform.UniformCrossover(self.UNIFORM)
        else:
            raise ValueError("crossover '" + crossover_name + ' is not found')
