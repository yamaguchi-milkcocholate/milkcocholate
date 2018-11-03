

class Situation:
    """
    遺伝子の要素がどの特徴量を意味するのか
    遺伝子の要素が取り得る値の範囲を表すクラス
    遺伝子の取り方は適応度関数によって決まるのでidを持つ
    """

    def __init__(self):
        self._fitness_function_id = None
        self._genomes = list()
        self._genome_ranges = dict()

    def set_fitness_function_id(self, f_id):
        """
        データベースのテーブル'fitness_function'のidをセットする
        :param f_id: int fitness_function_id
        """
        self._fitness_function_id = f_id

    def set_genome_ranges(self, **kwargs):
        """
        順番が保持されないので非推奨
        特徴量の名称 = tuple(取り得る範囲)を可変長で受け取る
        :param kwargs: dict  特徴量と範囲のdictionary
        """
        for key in kwargs:
            self._genomes.append(key)
        self._genome_ranges = kwargs

    def set_genome_ranges_with_order_dict(self, genome_ranges):
        """
        遺伝子と遺伝子の特徴・範囲を対応させる
        :param genome_ranges: collection.OrderedDict  順番を持たせたdictionary
        :return:
        """
        self._genome_ranges = genome_ranges
        for key in genome_ranges:
            self._genomes.append(key)

    def get_fitness_function(self):
        return self._fitness_function_id

    def get_genomes(self):
        return self._genomes

    def get_genome_ranges(self):
        return self._genome_ranges

    def range_to_tuple_list(self):
        """
        範囲をtupleで表して、それを配列でまとめたものを返す
        以前はこの形式で情報を交換していたことからの下位互換のようなもの
        :return: list (tuple[])
        """
        tuple_list = list()
        for key in self._genome_ranges:
            tuple_list.append(self._genome_ranges[key])
        return tuple_list
