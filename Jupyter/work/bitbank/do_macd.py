from modules.trader.macd import MACDTrader


trader = MACDTrader(is_exist_pickle=True)
trader.set_genome(host='localhost', population_id=431, individual_num=0)
trader()
