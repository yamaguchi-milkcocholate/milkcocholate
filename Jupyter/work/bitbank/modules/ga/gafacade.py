from modules.ga import sga, uniformcrossover


class Facade:

    def __init__(self, situation, fitness_function, population, mutation, cross, elite_num):
        """
        :param situation:          genofeature.Situation      特徴量を表すクラスのインスタンス
        :param fitness_function:   fitnessfunction.object     適応度関数を表すクラスのインスタンス
        :param population:         int                        個体数
        :param mutation:           int                        突然変異を起こすパーセンテージ
        :param cross:              int                        交叉が起きるパーセンテージ
        :param elite_num:          int                        次の世代に残すエリートの個体数
        """
        self._ga = [
            'sga',
            'uniform_crossover'
        ]
        self._siuation = situation
        self._fitness_function = fitness_function
        self._population = population
        self._mutation = mutation
        self._cross = cross
        self._elite_num = elite_num

    def select_department(self, ga_name):
        """

        :param ga_name:
        :return:
        """
        if ga_name is self._ga[0]:
            return sga.SimpleGeneticAlgorithm(
                situation=self._siuation, fitness_function=self._fitness_function, population=self._population,
                mutation=self._mutation, cross=self._cross, elite_num=self._elite_num
            )
        elif ga_name is self._ga[1]:
            return uniformcrossover.UniformCrossover(
                situation=self._siuation, fitness_function=self._fitness_function, population=self._population,
                mutation=self._mutation, cross=self._cross, elite_num=self._elite_num
            )
        else:
            raise ValueError("genetic algorithm '" + ga_name + "' is not found")
