from modules.fitnessfunction import simple_macd_params
from modules.fitnessfunction import bollingerband_linear_end


class Facade:
    SIMPLE_MACD_PARAMS = 1
    BOLLINGER_BAND_LINEAR_BAND = 2

    def __init__(self, candle_type):
        self._functions = [
            'simple_macd_params',
            'bollinger_band_linear_end',
        ]
        self._candle_type = candle_type

    def select_department(self, function_name, db_dept, hyper_params):
        """
        適応度関数を選ぶ
        :param function_name: string           適応度関数の名称
        :param db_dept:       Department       テーブルに対して操作を行うクラスのインスタンス
        :param hyper_params:  dict             ハイパーパラメータ
        :return:              FitnessFunction  適応度関数のインスタンス
        """
        if function_name is self._functions[0]:
            return simple_macd_params.SimpleMacDParams(
                candle_type=self._candle_type,
                db_dept=db_dept,
            )
        elif function_name is self._functions[1]:
            return bollingerband_linear_end.BollingerBandLinearEnd(
                candle_type=self._candle_type,
                db_dept=db_dept,
                hyper_params=hyper_params
            )
        else:
            raise ValueError("fitness function '" + function_name + "' is not found")
