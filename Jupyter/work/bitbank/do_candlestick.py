from modules.datamanager import savecandlestick


save_candle_data = savecandlestick.SaveCandlestick()
start_day = '20180601'
finish_day = '20181231'
pair = 'xrp_jpy'
timespace = '15min'
folder = 'validation_xrp'
save_candle_data.save_candlestick(
    timespace=timespace,
    start_day=start_day,
    finish_day=finish_day,
    pair=pair,
    folder=folder
)
