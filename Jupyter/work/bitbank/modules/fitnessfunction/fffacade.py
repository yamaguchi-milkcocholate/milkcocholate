from modules.fitnessfunction import simple_macd_params
from modules.fitnessfunction import bollingerband
from modules.fitnessfunction import bollingerband_period_goal
from modules.fitnessfunction import bollingerband_period_goal_ti


class Facade:
    SIMPLE_MACD_PARAMS = 1
    BOLLINGER_BAND_LINEAR_BAND = 2
    BOLLINGER_BAND_LINEAR_BAND_PERIOD_GOAL = 3
    BOLLINGER_BAND_LINEAR_BAND_PERIOD_GOAL_TI = 4

    def __init__(self, candle_type, pair):
        self._functions = [
            'simple_macd_params',
            'bollinger_band',
            'bollinger_band_period_goal',
            'bollinger_band_period_goal_ti',
        ]
        self._candle_type = candle_type
        self._pair = pair

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
                pair=self._pair
            )
        elif function_name is self._functions[1]:
            return bollingerband.BollingerBand(
                candle_type=self._candle_type,
                db_dept=db_dept,
                hyper_params=hyper_params,
                pair=self._pair
            )
        elif function_name is self._functions[2]:
            return bollingerband_period_goal.BollingerBandPeriodGoal(
                candle_type=self._candle_type,
                db_dept=db_dept,
                hyper_paras=hyper_params,
                pair=self._pair
            )
        elif function_name is self._functions[3]:
            return bollingerband_period_goal_ti.BollingerBandPeriodGoalTi(
                candle_type=self._candle_type,
                db_dept=db_dept,
                hyper_paras=hyper_params,
                pair=self._pair
            )
        else:
            raise ValueError("fitness function '" + function_name + "' is not found")
