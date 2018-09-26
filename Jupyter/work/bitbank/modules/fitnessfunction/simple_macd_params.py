from modules.datamanager import macd
from modules.datamanager import picker
import numpy as np


class SimpleMacDParams:
    BIT_BANK_CANDLE_STICK = ['5min', '15min', '1hour']

    def __init__(self, candle_type):
        if candle_type in SimpleMacDParams.BIT_BANK_CANDLE_STICK:
            self.picker = picker.Picker(candle_type)
            self.candlestick = self.picker.get_candlestick()
            self.approach = macd.MacD(self.candlestick)
        else:
            raise TypeError('candle type is not found')

    def calc_fitness(self, geno_type):
        population = geno_type.shape[0]
        fitness_list = list()
        for geno_i in range(population):
            geno = geno_type[geno_i]
            data = self.approach(geno[0], geno[1], geno[2])
            fitness_result = self.calc_result(data)
            fitness_list.append(fitness_result)
        return np.asarray(fitness_list, int)

    def calc_result(self, data):

        return 1
