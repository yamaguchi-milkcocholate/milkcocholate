from modules.datamanager import savecandlestick


save_candle_data = savecandlestick.SaveCandlestick()
start_day = '20190101'
finish_day = '20190101'
pair = 'xrp_jpy'
timespace = '5min'
folder = 'validation_xrp'
save_candle_data.save_candlestick(
    timespace=timespace,
    start_day=start_day,
    finish_day=finish_day,
    pair=pair,
    folder=folder
)
