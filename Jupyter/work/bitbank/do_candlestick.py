from modules.datamanager import savecandlestick


save_candle_data = savecandlestick.SaveCandlestick()
start_day = '20190111'
finish_day = '20190205'
pair = 'xrp_jpy'
timespace = '15min'
folder = 'data_xrp'
save_candle_data.save_candlestick(
    timespace=timespace,
    start_day=start_day,
    finish_day=finish_day,
    pair=pair,
    folder=folder
)
