from modules.fitnessfunction import simple_macd_params


class Facade:

    def __init__(self, candle_type):
        self._functions = [
            'simple_macd_params',
        ]
        self._candle_type = candle_type

    def select_department(self, function_name):
        """
        適応度関数を選ぶ
        :param function_name: string           適応度関数の名称
        :return:              Department like  適応度関数のインスタンス
        """
        if function_name is self._functions[0]:
            return simple_macd_params.SimpleMacDParams(self._candle_type)
        else:
            raise ValueError("fitness function '" + function_name + "' is not found")
