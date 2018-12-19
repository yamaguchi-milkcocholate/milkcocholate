import sys
import os
import unittest
import random
import numpy as np
sys.path.append(os.pardir + '/../')
from modules.gp.functions import *
from modules.datamanager.picker import Picker
from modules.datamanager.bollingerband import BollingerBand


class TestFunctions(unittest.TestCase):

    def setUp(self):
        self.picker = Picker(
            '5min',
            use_of_data='validation',
            coin='xrp',
            is_inclination=True
        )

    def tearDown(self):
        pass

    def test_show_wave(self):
        data = np.random.rand(20)
        data = 37.0 + data * 2
        # show_wave(data=data)

    def test_diff(self):
        data = np.random.rand(20)
        data = 37.0 + data * 2
        f = data
        data = diff(data=data)
        # show_wave(f=f, df=data)

    def test_template(self):
        data_0 = template(9, 0)
        data_1 = template(9, 1)
        data_2 = template(9, 2)
        data_3 = template(9, 3)
        data_4 = template(9, 4)
        data_5 = template(9, 5)
        data_6 = template(9, 6)
        data_7 = template(9, 7)
        """
        show_wave(
            template_0=data_0,
            template_1=data_1,
            template_2=data_2,
            template_3=data_3,
            template_4=data_4,
            template_5=data_5,
            template_6=data_6,
            template_7=data_7
        )
        """
        data_0 = diff(data=data_0)
        data_1 = diff(data=data_1)
        data_2 = diff(data=data_2)
        data_3 = diff(data=data_3)
        data_4 = diff(data=data_4)
        data_5 = diff(data=data_5)
        data_6 = diff(data=data_6)
        data_7 = diff(data=data_7)
        """
        show_wave(
            template_0=data_0,
            template_1=data_1,
            template_2=data_2,
            template_3=data_3,
            template_4=data_4,
            template_5=data_5,
            template_6=data_6,
            template_7=data_7
        )
        """

    def test_candlestick(self):
        candlestick = self.picker.get_candlestick()
        candlestick = candlestick.loc[:10].end.values
        data = diff(data=candlestick)
        data_7 = template(9, 7)
        diff_7 = diff(data=data_7)
        """
        show_wave(
            candlestick=candlestick,
            data=data,
            template=data_7,
            template_diff=diff_7
        )
        """

    def test_normalize(self):
        candlestick = self.picker.get_candlestick()
        candlestick = candlestick.loc[:10].end.values
        data = normalize(data=candlestick)
        data_7 = template(9, 2)
        diff_7 = normalize(data=data_7)
        """
        show_wave(
            candlestick=candlestick,
            data=data,
            template=data_7,
            template_diff=diff_7
        )
        """

    def test_cosine_similarity(self):
        candlestick = self.picker.get_candlestick()
        candlestick = candlestick.loc[:10].end.values
        data = template(10, 2)
        sim = cosine_similarity(data, candlestick)
        print(sim)
        x = np.asarray([1, 0, 0])
        y = np.asarray([0.5, 0, 0])
        sim = cosine_similarity(x, y)
        self.assertAlmostEqual(1, sim)

    def test_correlation_coefficient(self):
        candlestick = self.picker.get_candlestick()
        candlestick = candlestick.loc[:10].end.values
        data = template(10, 2)
        sim = correlation_coefficient(data, candlestick)
        print(sim)
        x = np.asarray([1, 0, 0])
        y = np.asarray([0.5, 0, 0])
        sim = correlation_coefficient(x, y)
        self.assertAlmostEqual(1, sim)

    def test_deviation_pattern_similarity(self):
        candlestick = self.picker.get_candlestick()
        candlestick = candlestick.loc[:10].end.values
        data = template(10, 2)
        sim = deviation_pattern_similarity(data, candlestick)
        print(sim)
        x = np.asarray([1, 0, 0])
        y = np.asarray([0.5, 0, 0])
        sim = deviation_pattern_similarity(x, y)
        self.assertAlmostEqual(1, sim)

    def test_pattern_analysis(self):
        candlestick = self.picker.get_candlestick()
        term = 10
        for i in range(0):
            start = random.randint(0, len(candlestick) - term)
            data = candlestick.loc[start:start + term].end.values
            print()
            sim = pattern_analysis(data)
            print(sim)
            tpl = template(size=len(data), number=sim)
            show_wave(
                data=tpl,
                candlestick=data
            )
        data = np.asarray([1, 1, 1])
        sim = pattern_analysis(data)
        print(sim)

        bollingerband = BollingerBand(candlestick=candlestick)
        bollingerband = bollingerband(20, 20)
        for i in range(10):
            start = random.randint(0, len(candlestick) - term)
            data = bollingerband.loc[start:start + term].simple_moving_average.values
            print()
            sim = pattern_analysis(data)
            print(sim)
            tpl = template(size=len(data), number=sim)
            show_wave(
                data=tpl,
                candlestick=data
            )


if __name__ == '__main__':
    unittest.main()
