from modules.feature.genofeature import Situation
from modules.fitnessfunction.bollingerband import BollingerBand
from modules.fitnessfunction.bollingerband_period_goal import BollingerBandPeriodGoal
from modules.fitnessfunction.bollingerband_period_goal_ti import BollingerBandPeriodGoalTi
from collections import OrderedDict


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
    BollingerBandPeriodGoalTiの遺伝子情報を揃える関数
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

    ranges = (1, 3)
    situation_dict = OrderedDict()

    for bitcoin_i in range(len(bitcoin)):
        for inclination_i in range(len(inclination)):
            for cur_i in range(len(end_position)):
                for pre_i in range(len(end_position)):
                    situation_dict[
                       end_position[pre_i] + '-' +
                       end_position[cur_i] + '-' +
                       inclination[inclination_i] + '-' +
                       bitcoin[bitcoin_i]
                    ] = ranges
    situation = Situation()
    situation.set_fitness_function_id(f_id=BollingerBandPeriodGoalTi.FITNESS_FUNCTION_ID)
    situation.set_genome_ranges_with_order_dict(genome_ranges=situation_dict)
    return situation
