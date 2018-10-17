from modules.crossover import onepoint, uniform


class CrossoverFacade:

    def __init__(self):
        self._crossover = [
            'one_point',
            'uniform',
        ]

    def select_department(self, crossover_name):
        if crossover_name is self._crossover[0]:
            return onepoint.OnePointCrossover()
        elif crossover_name is self._crossover[1]:
            return uniform.UniformCrossover()
        else:
            raise ValueError("crossover '" + crossover_name + ' is not found')
