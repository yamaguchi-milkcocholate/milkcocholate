from flask_modules.loggraph.repository import exptrepo
from flask_modules.loggraph.repository import poprepo
from flask_modules.exceptions.dbhost import HostNotFoundException
from collections import OrderedDict


class BollingerBand:
    HEATMAP_DEFAULT_VALUE = 10

    def __init__(self, host):
        self.__host = host
        self.__genome = list()
        self.__situation = list()

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
                # テスト用に遺伝子を取り出す
                self.__genome.append(result['genome'])
                self.__situation.append(experiments[i].situation)
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
        axis = ['U', 'U_U', 'U_M', 'M_L', 'L_L', 'L']
        init_dict = OrderedDict()
        init_dict['xaxis'] = axis
        for i in range(len(axis)):
            init_dict[axis[i]] = dict({
                axis[0]: self.HEATMAP_DEFAULT_VALUE,
                axis[1]: self.HEATMAP_DEFAULT_VALUE,
                axis[2]: self.HEATMAP_DEFAULT_VALUE,
                axis[3]: self.HEATMAP_DEFAULT_VALUE,
                axis[4]: self.HEATMAP_DEFAULT_VALUE,
                axis[5]: self.HEATMAP_DEFAULT_VALUE,
            })
        result = dict()
        result['HE'] = init_dict
        result['E'] = init_dict
        result['F'] = init_dict
        result['S'] = init_dict
        result['HS'] = init_dict
        index = 0

        for key in situation:
            if '-H_E' in key:
                # Hyper Expansion
                # y: 前回, x:現在
                y_location, x_location = self.__location_pattern(key.replace('-H_E', ''))
                result['HE'][y_location][x_location] = genome[index]
            elif '-E' in key:
                # Expansion
                # y: 前回, x:現在
                y_location, x_location = self.__location_pattern(key.replace('-E', ''))
                result['E'][y_location][x_location] = genome[index]
            elif '-F' in key:
                # Flat
                # y: 前回, x:現在
                y_location, x_location = self.__location_pattern(key.replace('-F', ''))
                result['F'][y_location][x_location] = genome[index]
            elif '-S' in key:
                # Squeeze
                # y: 前回, x:現在
                y_location, x_location = self.__location_pattern(key.replace('-S', ''))
                result['S'][y_location][x_location] = genome[index]
            elif '-H_S' in key:
                # Hyper Squeeze
                # y: 前回, x:現在
                y_location, x_location = self.__location_pattern(key.replace('-H_S', ''))
                result['HS'][y_location][x_location] = genome[index]
            else:
                raise TypeError('invalid')
            index += 1
        return result

    def __location_pattern(self, pattern):
        """
        前回と現在のボラティリティと終値の位置をsituationインスタンスのキーから特定する
        :param pattern: 前回と現在の位置を特定するためのキー
        :return: 前回の位置を現す文字列, 現在の位置を表す文字列
        """
        # 分岐の順番は重要! U-はU_U-を含んでしまうなど
        if 'U_U-' in pattern:
            return 'U_U', self.__end_location_pattern(pattern.replace('U_U-', ''))
        elif 'U_M-' in pattern:
            return 'U_M', self.__end_location_pattern(pattern.replace('U_M-', ''))
        elif 'M_L-' in pattern:
            return 'M_L', self.__end_location_pattern(pattern.replace('M_L-', ''))
        elif 'L_L-' in pattern:
            return 'L_L', self.__end_location_pattern(pattern.replace('L_L-', ''))
        elif 'U-' in pattern:
            return 'U', self.__end_location_pattern(pattern.replace('U-', ''))
        elif 'L-' in pattern:
            return 'L', self.__end_location_pattern(pattern.replace('L-', ''))
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
            return 'U_U'
        elif 'U_M' in pattern:
            return 'U_M'
        elif 'M_L' in pattern:
            return 'M_L'
        elif 'L_L' in pattern:
            return 'L_L'
        elif 'U' in pattern:
            return 'U'
        elif 'L' in pattern:
            return 'L'
        else:
            raise TypeError('invalid')

    def get_genome(self):
        """
        テスト用のゲッター
        :return: array: 全てのエリート遺伝子
        """
        return self.__genome

    def get_situation(self):
        """
        テスト用のゲッター
        :return: array: 遺伝子情報
        """
        return self.__situation
