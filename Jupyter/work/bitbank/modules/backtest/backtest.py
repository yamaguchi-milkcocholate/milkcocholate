import datetime
import pickle
from modules.fitnessfunction import fffacade
from modules.crossover import cfacade
from modules.db import facade
from modules.ga import ga


class BackTest:
    DEFAULT_STEPS = 3000
    DEFAULT_LOG_SPAN = 20

    def __init__(self, situation, candle_type, pair, population, mutation,
                 cross, elite_num, host, fitness_function_name, crossover_name, hyper_params=None):
        """
        :param situation:                Situation 遺伝子の要素の取りうる範囲などを表す
        :param candle_type:              string    ロウソク足データの種類
        :param pair:                     string    コインの種類
        :param population:               int       個体数
        :param mutation:                 int       突然変異のパーセンテージ
        :param cross:                    int       交叉のパーセンテージ
        :param elite_num:                int       世代交代時に残すエリート個体数
        :param host:                     string    dbの接続先
        :param fitness_function_name:    string    適応度関数の名称
        :param crossover_name:           string    交叉手法の名称
        :param hyper_params:             dict      ハイパーパラメータ
        """
        self._db_facade = facade.Facade(host=host)
        ff_facade = fffacade.Facade(candle_type=candle_type, coin=pair)
        c_facade = cfacade.CrossoverFacade()
        expt_logs_dept = self._db_facade.select_department('experiment_logs')
        # 適応度関数
        fitness_function = ff_facade.select_department(
            function_name=fitness_function_name,
            db_dept=expt_logs_dept,
            hyper_params=hyper_params
        )
        # 交叉手法
        crossover_method = c_facade.select_department(
            crossover_name=crossover_name
        )
        self._ga = ga.GeneticAlgorithm(
            mutation=mutation,
            cross=cross,
            situation=situation,
            elite_num=elite_num,
            population=population,
            crossover_method=crossover_method,
            fitness_function=fitness_function
        )
        self._hyper_params = hyper_params
        self.__pair = pair

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
        self._ga.generation(steps=steps, experiment_id=experiment_id, log_span=log_span,
                            population_dept=population_dept)
        end_at = datetime.datetime.now()
        # 実験を記録
        expt_dept = self._db_facade.select_department('experiments')
        execute_time = int(end_at.timestamp()) - int(start_at.timestamp())
        # ハイパーパラメータがあればバイナリに変換する
        if self._hyper_params is not None:
            self._hyper_params = pickle.dumps(self._hyper_params)
        else:
            self._hyper_params = pickle.dumps(dict())
        values = [
            self.__pair,
            self._ga.get_crossover_id(),
            self._ga.get_fitness_function_id(),
            pickle.dumps(self._ga.get_situation().get_genome_ranges()),
            self._hyper_params,
            self._ga.get_mutation(),
            self._ga.get_cross(),
            self._ga.get_population(),
            self._ga.get_elite_num(),
            start_at.strftime(str_format),
            end_at.strftime(str_format),
            execute_time,
        ]
        expt_dept.give_writer_task([values])

