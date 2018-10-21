import unittest
import sys
import os
import pandas as pd
sys.path.append(os.pardir+'/../')
from modules.datamanager import savecandledata


class TestGetVariable(unittest.TestCase):

    def setUp(self):
        self.bar = savecandledata.SaveCandleData()

    def test_save_candledata(self):
        self.bar.save_candledata("1hour", "20181001", "20181007", "btc_jpy")
        test_list = self.bar.get_test_list()
        list_len = len(test_list)

        test_dict = {"candlestick": [{"type": "1hour", "ohlcv": [
            ["746602", "751299", "746602", "750895", "68.5374", 1538697600000],
            ["750834", "750900", "748500", "749070", "55.6426", 1538701200000],
            ["749070", "749354", "742609", "744193", "114.1167", 1538704800000],
            ["744249", "745930", "743834", "744831", "41.2794", 1538708400000],
            ["744800", "746292", "744000", "745412", "41.0597", 1538712000000],
            ["745418", "745760", "744132", "745269", "26.7986", 1538715600000],
            ["745391", "747700", "744686", "747044", "48.1305", 1538719200000],
            ["746931", "747228", "744436", "744998", "92.9565", 1538722800000],
            ["744993", "745899", "744020", "744248", "39.9088", 1538726400000],
            ["744107", "745041", "743200", "745041", "30.3970", 1538730000000],
            ["745041", "745591", "744118", "744228", "35.4777", 1538733600000],
            ["744220", "746487", "744210", "746073", "36.5314", 1538737200000],
            ["746044", "746569", "745274", "745300", "56.9851", 1538740800000],
            ["745300", "746994", "745289", "745447", "25.6731", 1538744400000],
            ["745446", "746759", "744799", "746583", "28.2339", 1538748000000],
            ["746431", "746685", "745000", "745037", "27.9641", 1538751600000],
            ["745318", "746400", "743740", "744546", "25.7447", 1538755200000],
            ["744443", "744798", "743709", "744101", "18.7177", 1538758800000],
            ["744101", "745300", "743490", "744950", "12.6881", 1538762400000],
            ["744950", "745876", "743817", "744764", "17.4417", 1538766000000],
            ["744750", "745631", "743026", "744927", "26.9554", 1538769600000],
            ["744929", "746500", "743830", "746009", "33.6841", 1538773200000],
            ["746004", "754795", "746004", "749228", "141.0846", 1538776800000],
            ["749228", "750555", "746962", "749558", "33.8135", 1538780400000]]}],
                     "timestamp": 1538783999930}
        candlestick = test_dict['candlestick'][0]['ohlcv']
        df = pd.DataFrame(candlestick, columns=['open', 'high', 'low', 'end', 'turnover', 'time'])
        df['time'] = pd.to_datetime(df['time'], unit='ms')
        print(df.equals(test_list[4]))
        self.assertEqual(list_len, 7)

        # 20181005日のデータが一致するかの確認
        # 保存した期間の長さの確認

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
