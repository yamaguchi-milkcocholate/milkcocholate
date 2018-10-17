from modules.fitnessfunction import simple_macd_params


class Facade:
    SIMPLE_MACD_PARAMS = 1

    def __init__(self, candle_type):
        self._functions = [
            'simple_macd_params',
        ]
        self._candle_type = candle_type

    def select_department(self, function_name, db_dept):
        """
        適応度関数を選ぶ
        :param function_name: string           適応度関数の名称
        :param db_dept:       Department       テーブルに対して操作を行うクラスのインスタンス
        :return:              FitnessFunction  適応度関数のインスタンス
        """
        if function_name is self._functions[0]:
            return simple_macd_params.SimpleMacDParams(
                candle_type=self._candle_type, db_dept=db_dept, fitness_function_id=self.SIMPLE_MACD_PARAMS)
        else:
            raise ValueError("fitness function '" + function_name + "' is not found")
