import datetime
import pickle
from modules.fitnessfunction import fffacade
from modules.db import facade
from modules.crossover import uniform
from modules.ga import ga


class UniformCrossoverMacd:
    """
    一様交叉を使って、MACDのパラメータを最適化する
    """
    DEFAULT_STEPS = 300
    DEFAULT_LOG_SPAN = 20
    GENETIC_ALGORITHM_ID = 2
    FITNESS_FUNCTION_ID = 1
    FITNESS_FUNCTION_NAME = 'simple_macd_params'

    def __init__(self, situation, candle_type, population, mutation, cross, elite_num, host):
        """
        :param situation:     Situation 遺伝子の要素の取りうる範囲などを表す
        :param candle_type:   string    ロウソク足データの種類
        :param population:    int       個体数
        :param mutation:      int       突然変異のパーセンテージ
        :param cross:         int       交叉のパーセンテージ
        :param elite_num:     int       世代交代時に残すエリート個体数
        :param host:  string dbの接続先
        """
        self._db_facade = facade.Facade(host=host)
        ff_facade = fffacade.Facade(candle_type=candle_type)
        expt_logs_dept = self._db_facade.select_department('experiment_logs')
        fitness_function = ff_facade.select_department(function_name=self.FITNESS_FUNCTION_NAME, db_dept=expt_logs_dept)
        crossover_method = uniform.UniformCrossover()
        self._ga = ga.GeneticAlgorithm(
            mutation=mutation,
            cross=cross,
            situation=situation,
            elite_num=elite_num,
            population=population,
            crossover_method=crossover_method,
            fitness_function=fitness_function
        )

    def __call__(self, steps=DEFAULT_STEPS, log_span=DEFAULT_LOG_SPAN):
        """
       バックテスト
       :param steps: int     世代交代数
       :param log_span: int    どのくらいの期間ごとに記録を取るか
       """
        experiment_id = self._db_facade.select_department('experiments').make_writer_find_next_id()
        population_dept = self._db_facade.select_department('populations')
        str_format = '%Y-%m-%d %H:%M:%S'
        start_at = datetime.datetime.now()
        self._ga.generation(steps=steps, experiment_id=experiment_id, log_span=log_span, population_dept=population_dept)
        end_at = datetime.datetime.now()
        # 実験を記録
        expt_dept = self._db_facade.select_department('experiments')
        execute_time = int(start_at.strftime('%s')) - int(end_at.strftime('%s'))
        values = [
            self.GENETIC_ALGORITHM_ID,
            self.FITNESS_FUNCTION_ID,
            pickle.dumps(self._ga.get_situation()),
            self._ga.get_mutation(),
            self._ga.get_cross(),
            self._ga.get_population(),
            self._ga.get_elite_num(),
            start_at.strftime(str_format),
            end_at.strftime(str_format),
            execute_time,
        ]
        expt_dept.give_writer_task(values)
