import os
import sys
import pprint
import datetime
import pickle
sys.path.append(os.pardir)
from modules.ga import sga
from modules.fitnessfunction import fffacade
from modules.db import facade


class SgaMacd:
    """
    SGAを使って、MACDのパラメータを最適化する
    """
    DEFAULT_STEPS = 300
    GENETIC_ALGORITHM_ID = 1
    FITNESS_FUNCTION_ID = 1
    GENETIC_ALGORITHM_NAME = 'uniform_crossover'
    FITNESS_FUNCTION_NAME = 'simple_macd_params'

    def __init__(self, situation, candle_type, population, mutation, cross, elite_num):
        """
        :param situation:     Situation 遺伝子の要素の取りうる範囲などを表す
        :param candle_type:   string    ロウソク足データ
        :param population:    int       個体数
        :param mutation:      int       突然変異のパーセンテージ
        :param cross:         int       交叉のパーセンテージ
        :param elite_num:     int       世代交代時に残すエリート個体数
        """
        ff_facade = fffacade.Facade(candle_type=candle_type)
        fitness_function = ff_facade.select_department(self.FITNESS_FUNCTION_NAME)
        self.ga = sga.SimpleGeneticAlgorithm(situation=situation, population=population,
                                             fitness_function=fitness_function, mutation=mutation,
                                             cross=cross, elite_num=elite_num)
        self._situation = situation
        self._population = population
        self._mutation = mutation
        self._cross = cross
        self._elite_num = elite_num

    def __call__(self, host, steps=DEFAULT_STEPS):
        """
        バックテスト
        :param host:  string dbの接続先
        :param steps: int    世代交代数
        """
        str_format = '%Y-%m-%d %H:%M:%S'
        start_at = datetime.datetime.now()
        self.ga(steps)
        end_at = datetime.datetime.now()
        print('geno_type')
        pprint.pprint(self.ga.geno_type)
        print('fitness')
        pprint.pprint(self.ga.fitness)
        db_facade = facade.Facade(host)
        # 実験を記録
        dept = db_facade.select_department('experiments')
        execute_time = int(start_at.strftime('%s')) - int(end_at.strftime('%s'))
        values = [
            self.GENETIC_ALGORITHM_id,
            self.FITNESS_FUNCTION_ID,
            pickle.dumps(self._situation),
            self._mutation,
            self._cross,
            self._population,
            self._elite_num,
            start_at.strftime(str_format),
            end_at.strftime(str_format),
            execute_time,
        ]
        dept.give_writer_task(values)

