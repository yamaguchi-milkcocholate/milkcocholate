from modules.trader.macd import MACDTrader


trader = MACDTrader(is_exist_pickle=True)
trader.set_genome(host='localhost', population_id=420)
trader()
