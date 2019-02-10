import random


class Condition:

    def __init__(self):
        self.technical_analysis = list()
        self.tech_list = list()

    def add_technical_analysis(self, name, lower_limit, upper_limit):
        """
        テクニカル分析指標を追加する
        :param name:         string    名称
        :param lower_limit:  float|int 下限
        :param upper_limit:  float|int 上限
        """
        if type(name) is not str:
            raise TypeError('name must be string')

        self.technical_analysis.append({
            'name': name,
            'lower_limit': lower_limit,
            'upper_limit': upper_limit
        })
        self.tech_list.append(name)

    def random_choice(self):
        """
        ランダムなテクニカル分析指標を返す
        :return: dict
        """
        return self.technical_analysis[random.randint(0, len(self.technical_analysis) - 1)]

    def get_technical_analysis(self):
        return self.technical_analysis

    def get_tech_list(self):
        return self.tech_list
