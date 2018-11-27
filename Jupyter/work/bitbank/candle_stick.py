from modules.datamanager import savecandledata


save_candle_data = savecandledata.SaveCandleData()
start_day = '20181101'
finish_day = '20181126'
pair = 'btc_jpy'
timespace = '5min'
folder = 'validation'
save_candle_data.save_candledata(
    timespace=timespace,
    start_day=start_day,
    finish_day=finish_day,
    pair=pair,
    folder=folder
)
