from modules.datamanager import savecandledata


save_candle_data = savecandledata.SaveCandleData()
timespace = '1hour'
start_day = '20180201'
finish_day = '20181025'
pair = 'btc_jpy'
save_candle_data.save_candledata(
    timespace=timespace,
    start_day=start_day,
    finish_day=finish_day,
    pair=pair
)

timespace = '15min'
save_candle_data.save_candledata(
    timespace=timespace,
    start_day=start_day,
    finish_day=finish_day,
    pair=pair
)

timespace = '5min'
save_candle_data.save_candledata(
    timespace=timespace,
    start_day=start_day,
    finish_day=finish_day,
    pair=pair
)
