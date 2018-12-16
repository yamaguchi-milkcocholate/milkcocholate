import random


class Condition:

    def __init__(self):
        self.technical_analysis = list()

    def add_technical_analysis(self, name, lower_limit, upper_limit):
        """
        テクニカル分析指標を追加する
        :param name:         string    名称
        :param lower_limit:  float|int 下限
        :param upper_limit:  float|int 上限
        """
        if type(name) is not str:
            raise TypeError('name must be string')
        if not (type(lower_limit) is float or type(lower_limit) is int):
            raise TypeError('lower_limit must be float or int')
        if not (type(upper_limit) is float or type(upper_limit) is int):
            raise TypeError('lower_limit must be float or int')

        self.technical_analysis.append({
            'name': name,
            'lower_limit': lower_limit,
            'upper_limit': upper_limit
        })

    def random_choice(self):
        """
        ランダムなテクニカル分析指標を返す
        :return: dict
        """
        return self.technical_analysis[random.randint(0, len(self.technical_analysis) - 1)]
