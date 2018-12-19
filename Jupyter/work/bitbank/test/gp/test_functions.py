import sys
import os
import unittest
import numpy as np
sys.path.append(os.pardir + '/../')
from modules.gp.functions import *


class TestFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_show_wave(self):
        data = np.random.rand(20)
        data = 37.0 + data * 2
        #show_wave(data=data)

    def test_diff(self):
        data = np.random.rand(20)
        data = 37.0 + data * 2
        f = data
        data = diff(data=data)
        #show_wave(f=f, df=data)

    def test_template(self):
        data_0 = template(9, 0)
        data_1 = template(9, 1)
        data_2 = template(9, 2)
        data_3 = template(9, 3)
        data_4 = template(9, 4)
        data_5 = template(9, 5)
        data_6 = template(9, 6)
        data_7 = template(9, 7)
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


if __name__ == '__main__':
    unittest.main()
