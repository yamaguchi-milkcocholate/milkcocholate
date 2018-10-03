from modules.ga import sga
from modules.fitnessfunction import simple_macd_params


class SgaMacd:
    DEFAULT_STEPS = 10000

    def __init__(self):
        situation = list()
        situation.append((1, 50))
        situation.append((2, 100))
        situation.append((1, 50))
        candle_type = '1hour'
        fitness_function = simple_macd_params.SimpleMacDParams(candle_type)
        self.ga = sga.SimpleGeneticAlgorithm(situation, population=11, fitness_function=fitness_function)

    def back_test(self, steps=DEFAULT_STEPS):
        self.ga(steps)

    def processing(self):
        pass


if __name__ == '__main__':
    sga_macd = SgaMacd()
    sga_macd.back_test(1000)
    print(sga_macd.ga.geno_type)
    print(sga_macd.ga.fitness)

