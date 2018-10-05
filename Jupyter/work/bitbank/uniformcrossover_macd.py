from modules.ga import uniformcrossover
from modules.fitnessfunction import simple_macd_params


class UniformCrossoverMacd:
    DEFAULT_STEPS = 300

    def __init__(self):
        situation = list()
        situation.append((1, 20))
        situation.append((20, 40))
        situation.append((1, 15))
        candle_type = '15min'
        fitness_function = simple_macd_params.SimpleMacDParams(candle_type)
        self.ga = uniformcrossover.UniformCrossover(situation, fitness_function, population=15,
                                                    mutation=2, cross=50, elite_num=1)

    def back_test(self, steps=DEFAULT_STEPS):
        self.ga(steps)

    def procession(self):
        pass


if __name__ == '__main__':
    uniformcrossover_macd = UniformCrossoverMacd()
    uniformcrossover_macd.back_test()
    print(uniformcrossover_macd.ga.geno_type)
    print(uniformcrossover_macd.ga.fitness)
