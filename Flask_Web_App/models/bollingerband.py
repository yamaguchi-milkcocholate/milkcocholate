from flask_modules.loggraph.repository import exptrepo
from flask_modules.loggraph.repository import poprepo
from flask_modules.exceptions.dbhost import HostNotFoundException


class BollingerBandController:

    def __init__(self, host):
        self.__host = host

    def __call__(self):
        """
        :return:
        [
            {'experiment: Experiment, max_fitness: int},
            {'experiment: Experiment, max_fitness: int},
        ]
        """
        try:
            pop_repository = poprepo.PopulationRepository(host=self.__host)
            expt_repository = exptrepo.ExperimentRepository(host=self.__host)
            experiments = expt_repository.get_bollinger_band()
            bollingerbands = list()
            for i in range(len(experiments)):
                el = dict()
                el['experiment'] = experiments[i]
                result = pop_repository.find_max_fitness_and_genome(experiment_id=experiments[i].id)
                el['max_fitness'] = result['fitness']
                inclination_pattern = self.__inclination_pattern(
                    genome=result['genome'],
                    situation=experiments[i].situation
                )
                max_genome = dict()
                max_genome['inclination_patterm'] = inclination_pattern
                el['max_genome'] = max_genome
                bollingerbands.append(el)
            return bollingerbands
        except HostNotFoundException:
            raise

    def __inclination_pattern(self, genome, situation):
        """
        Hyper Expansion
        Expansion
        Flat
        Squeeze
        Hyper Squeeze
        :param:  genome      numpy
        :param:  situation   collections.OrderedDict
        :return:             dictionary
        {
            'HE' : {

            },
            'E' : {

            },
            'F' : {

            },
            'S' : {

            },
            'HS' : {

            },
        }
        """
        result = dict()
        result['HE'] = dict()
        result['E'] = dict()
        result['F'] = dict()
        result['S'] = dict()
        result['HS'] = dict()
        index = 0

        for key in situation:
            if '-H_E' in key:
                # Hyper Expansion
                result['HE'][self.__start_location_pattern(key.replace('-H_E', ''))] = genome[index]
            elif '-E' in key:
                # Expansion
                result['E'][self.__start_location_pattern(key.replace('-E', ''))] = genome[index]
            elif '-F' in key:
                # Flat
                result['F'][self.__start_location_pattern(key.replace('-F', ''))] = genome[index]
            elif '-S' in key:
                # Squeeze
                result['S'][self.__start_location_pattern(key.replace('-S', ''))] = genome[index]
            elif '-H_S' in key:
                # Hyper Squeeze
                result['HS'][self.__start_location_pattern(key.replace('-H_S', ''))] = genome[index]
            else:
                raise TypeError('invalid')
            index += 1
        return result

    def __start_location_pattern(self, pattern):
        """
        前回と現在のボラティリティと終値の位置をsituationインスタンスのキーから特定する
        この関数では前回の位置を特定して、さらに現在の位置を特定する関数を呼ぶ。
        :param pattern: 前回と現在の位置を特定するためのキー
        :return: 前回と現在の位置を現す文字列(キー)
        """
        # 分岐の順番は重要! U_はU-U_を含んでしまうなど
        if 'U_U-' in pattern:
            return '1' + ' to ' + self.__end_location_pattern(pattern.replace('U-U_', ''))
        elif 'U_M-' in pattern:
            return '2' + ' to ' + self.__end_location_pattern(pattern.replace('U-M_', ''))
        elif 'M_L-' in pattern:
            return '3' + ' to ' + self.__end_location_pattern(pattern.replace('M-L_', ''))
        elif 'L_L-' in pattern:
            return '4' + ' to ' + self.__end_location_pattern(pattern.replace('L-L_', ''))
        elif 'U-' in pattern:
            return '5' + ' to ' + self.__end_location_pattern(pattern.replace('U_', ''))
        elif 'L-' in pattern:
            return '6' + ' to ' + self.__end_location_pattern(pattern.replace('L_', ''))
        else:
            raise TypeError('invalid')

    @staticmethod
    def __end_location_pattern(pattern):
        """
        現在のボラティリティーと終値の位置を特定する関数
        :param pattern: 現在の位置を特定するためのキー
        :return: 前回と現在の位置を表す文字列(キー)
        """
        # 分岐の順番は重要! UはU-Uを含んでしまうなど
        if 'U_U' in pattern:
            return '1'
        elif 'U_M' in pattern:
            return '2'
        elif 'M_L' in pattern:
            return '3'
        elif 'L_L' in pattern:
            return '4'
        elif 'U' in pattern:
            return '5'
        elif 'L' in pattern:
            return '6'
        else:
            raise TypeError('invalid')
