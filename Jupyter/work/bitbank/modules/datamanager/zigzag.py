from modules.datamanager.picker import Picker


class ZigZag:

    def __init__(self, use_of_data='training'):
        picker = Picker(span='15min', use_of_data=use_of_data, coin='xrp')
        self.candlestick = picker.get_candlestick()

    def get_candlestick(self):
        return self.candlestick
