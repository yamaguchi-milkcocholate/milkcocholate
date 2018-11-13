from modules.db import crossoverdept, fitfuncdept, exptdept, exptlogsdept, popdept, realtimedept, realtimelogdept


class Facade:

    def __init__(self, host):
        self._tables = [
            'crossovers',
            'fitness_functions',
            'experiments',
            'experiment_logs',
            'populations',
            'realtime_tests',
            'realtime_test_logs',
        ]
        self._host = host

    def select_department(self, table):
        """
        各テーブルを操作するDepartmentクラスを返す
        :param table: string           テーブル名
        :return:      Department like  テーブルを操作するDepartmentクラス
        """
        if table is self._tables[0]:
            return crossoverdept.CrossoversDepartment(self._host)
        elif table is self._tables[1]:
            return fitfuncdept.FitnessFunctionsDepartment(self._host)
        elif table is self._tables[2]:
            return exptdept.ExperimentsDepartment(self._host)
        elif table is self._tables[3]:
            return exptlogsdept.ExperimentLogsDepartment(self._host)
        elif table is self._tables[4]:
            return popdept.PopulationsDepartment(self._host)
        elif table is self._tables[5]:
            return realtimedept.RealTimeTestDepartment(self._host)
        elif table is self._tables[6]:
            return realtimelogdept.RealTimeTestLogsDepartment(self._host)
        else:
            raise ValueError("table '" + table + "' is not found")
