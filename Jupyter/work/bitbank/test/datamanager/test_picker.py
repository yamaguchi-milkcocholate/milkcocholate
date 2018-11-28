import sys
import os
import unittest
sys.path.append(os.pardir+'/../')
from modules.datamanager import picker


class TestPicker(unittest.TestCase):

    def setUp(self):
        self._picker_1hour = picker.Picker('1hour', use_of_data='training', pair='btc')
        self._picker_15min = picker.Picker('15min', use_of_data='training', pair='btc')
        self._picker_5min = picker.Picker('5min', use_of_data='training', pair='btc')

    def test_load_data(self):
        data = self._picker_1hour.get_candlestick()
        print(data)
        data = self._picker_15min.get_candlestick()
        print(data)
        data = self._picker_5min.get_candlestick()
        print(data)


if __name__ == '__main__':
    unittest.main()
