from modules.feature.genofeature import Situation
from modules.fitnessfunction.bollingerband import BollingerBand
from modules.fitnessfunction.bollingerband_period_goal import BollingerBandPeriodGoal
from modules.fitnessfunction.bollingerband_period_goal_ti import BollingerBandPeriodGoalTi
from modules.fitnessfunction.wavetpl import WaveTemplate
from modules.fitnessfunction.macd import MACD_
from collections import OrderedDict

WAVE_TEMPLATE_NUM = 9


def bollinger_band():
    """
    BollingerBand, の遺伝子情報を揃える関数
    :return: Situation: 遺伝子情報を持つクラスのインスタンス
    """
    end_position = list()
    end_position.append('U')
    end_position.append('U_U')
    end_position.append('U_M')
    end_position.append('M_L')
    end_position.append('L_L')
    end_position.append('L')

    inclination = list()
    inclination.append('H_E')
    inclination.append('E')
    inclination.append('F')
    inclination.append('S')
    inclination.append('H_S')

    ranges = (1, 3)
    situation_dict = OrderedDict()

    for inclination_i in range(len(inclination)):
        for cur_i in range(len(end_position)):
            for pre_i in range(len(end_position)):
                situation_dict[
                   end_position[pre_i] + '-' +
                   end_position[cur_i] + '-' +
                   inclination[inclination_i]
                ] = ranges
    situation = Situation()
    situation.set_fitness_function_id(f_id=BollingerBand.FITNESS_FUNCTION_ID)
    situation.set_genome_ranges_with_order_dict(genome_ranges=situation_dict)
    return situation


def bollinger_band_period_goal():
    """
    BollingerBandPeriodGoalの遺伝子情報を揃える関数
    :return: Situation: 遺伝子情報を持つクラスのインスタンス
    """
    end_position = list()
    end_position.append('U')
    end_position.append('U_U')
    end_position.append('U_M')
    end_position.append('M_L')
    end_position.append('L_L')
    end_position.append('L')

    inclination = list()
    inclination.append('H_E')
    inclination.append('E')
    inclination.append('F')
    inclination.append('S')
    inclination.append('H_S')

    ranges = (1, 3)
    situation_dict = OrderedDict()

    for inclination_i in range(len(inclination)):
        for cur_i in range(len(end_position)):
            for pre_i in range(len(end_position)):
                situation_dict[
                   end_position[pre_i] + '-' +
                   end_position[cur_i] + '-' +
                   inclination[inclination_i]
                ] = ranges
    situation = Situation()
    situation.set_fitness_function_id(f_id=BollingerBandPeriodGoal.FITNESS_FUNCTION_ID)
    situation.set_genome_ranges_with_order_dict(genome_ranges=situation_dict)
    return situation


def bollinger_band_ti():
    """
    BollingerBandPeriodGoalTi, BollingerBandSAMTiの遺伝子情報を揃える関数
    :return: Situation: 遺伝子情報を持つクラスのインスタンス
    """
    end_position = list()
    end_position.append('U')
    end_position.append('U_U')
    end_position.append('U_M')
    end_position.append('M_L')
    end_position.append('L_L')
    end_position.append('L')

    inclination = list()
    inclination.append('H_E')
    inclination.append('E')
    inclination.append('F')
    inclination.append('S')
    inclination.append('H_S')

    bitcoin = list()
    bitcoin.append('Y')
    bitcoin.append('B')

    # 買い or 保持
    yen_ranges = (1, 2)
    # 売り or 保持
    coin_ranges = (2, 3)
    situation_dict = OrderedDict()

    for inclination_i in range(len(inclination)):
        for cur_i in range(len(end_position)):
            for pre_i in range(len(end_position)):
                situation_dict[
                   end_position[pre_i] + '-' +
                   end_position[cur_i] + '-' +
                   inclination[inclination_i] + '-' +
                   bitcoin[0]
                ] = yen_ranges

    for inclination_i in range(len(inclination)):
        for cur_i in range(len(end_position)):
            for pre_i in range(len(end_position)):
                situation_dict[
                   end_position[pre_i] + '-' +
                   end_position[cur_i] + '-' +
                   inclination[inclination_i] + '-' +
                   bitcoin[1]
                ] = coin_ranges
    situation = Situation()
    situation.set_fitness_function_id(f_id=BollingerBandPeriodGoalTi.FITNESS_FUNCTION_ID)
    situation.set_genome_ranges_with_order_dict(genome_ranges=situation_dict)
    return situation


def wave_template(waves, pattern_num):
    """
    波形テンプレート
    waves {
        'name' : size
    }
    :param waves:      dict
    :param pattern_num: int
    :return: Situation
    """

    situation_dict = OrderedDict()
    for pat_i in range(pattern_num):
        # 売りパターン
        for name in waves:
            for el_i in range(waves[name]):
                situation_dict[
                    str(pat_i) + '-SELL-' + name + '-' + str(el_i)
                ] = (0, WAVE_TEMPLATE_NUM)
        situation_dict[
            str(pat_i) + '-SELL-THRESHOLD'
        ] = (-1, 1)

        # 買うパターン
        for name in waves:
            for el_i in range(waves[name]):
                situation_dict[
                    str(pat_i) + '-BUY-' + name + '-' + str(el_i)
                ] = (0, WAVE_TEMPLATE_NUM)
        situation_dict[
            str(pat_i) + '-BUY-THRESHOLD'
        ] = (-1, 1)

    situation = Situation()
    situation.set_fitness_function_id(f_id=WaveTemplate.FITNESS_FUNCTION_ID)
    situation.set_genome_ranges_with_order_dict(genome_ranges=situation_dict)
    return situation


def macd():
    """
    MACD
    :return: Situation
    """
    # 下降トレンドで買うのでマイナス
    situation_dict = OrderedDict()
    situation_dict['BUY-15MIN-HISTOGRAM-DECREASE-RATE'] = (0, 1)   # 0
    situation_dict['BUY-15MIN-STEP-RATE'] = (0, 1)   # 1
    situation_dict['BUY-5MIN-HISTOGRAM-DECREASE-RATE'] = (0, 1)   # 2
    situation_dict['BUY-5MIN-STEP-RATE'] = (0, 1)   # 3
    situation_dict['BUY-15MIN-START-MACD'] = (-1, 1)   # 4
    situation_dict['BUY-15MIN-START-SIGNAL'] = (-1, 1)   # 5
    situation_dict['BUY-5MIN-START-MACD'] = (-1, 1)   # 6
    situation_dict['BUY-5MIN-START-SIGNAL'] = (-1, 1)   # 7
    situation_dict['BUY-15MIN-END-MACD'] = (-1, 1)   # 8
    situation_dict['BUY-15MIN-END-SIGNAL'] = (-1, 1)   # 9
    situation_dict['BUY-5MIN-END-MACD'] = (-1, 1)   # 10
    situation_dict['BUY-5MIN-END-SIGNAL'] = (-1, 1)   # 11

    # 上昇トレンドで売るのでプラス
    situation_dict['SELL-15MIN-HISTOGRAM-DECREASE-RATE'] = (0, 1)   # 12
    situation_dict['SELL-15MIN-STEP-RATE'] = (0, 1)   # 13
    situation_dict['SELL-5MIN-HISTOGRAM-DECREASE-RATE'] = (0, 1)   # 14
    situation_dict['SELL-5MIN-STEP-RATE'] = (0, 1)   # 15
    situation_dict['SELL-15MIN-START-MACD'] = (-1, 1)   # 16
    situation_dict['SELL-15MIN-START-SIGNAL'] = (-1, 1)   # 17
    situation_dict['SELL-5MIN-START-MACD'] = (-1, 1)   # 18
    situation_dict['SELL-5MIN-START-SIGNAL'] = (-1, 1)   # 19
    situation_dict['SELL-15MIN-END-MACD'] = (-1, 1)   # 20
    situation_dict['SELL-15MIN-END-SIGNAL'] = (-1, 1)   # 21
    situation_dict['SELL-5MIN-END-MACD'] = (-1, 1)   # 22
    situation_dict['SELL-5MIN-END-SIGNAL'] = (-1, 1)   # 23

    situation_dict['BUY-15MIN-MOUNT'] = (0, 1)   # 24
    situation_dict['SELL-15MIN-MOUNT'] = (0, 1)   # 25

    situation_dict['BUY-5MIN-MOUNT'] = (0, 1)   # 26
    situation_dict['SELL-5MIN-MOUNT'] = (0, 1)   # 27

    situation_dict['SELL-PRICE_RATE'] = (0, 1)   # 28

    situation = Situation()
    situation.set_fitness_function_id(f_id=MACD_.FITNESS_FUNCTION_ID)
    situation.set_genome_ranges_with_order_dict(genome_ranges=situation_dict)
    return situation
