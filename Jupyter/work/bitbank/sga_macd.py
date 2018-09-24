from modules.ga import sga
from modules.datamanager import macd
from modules.datamanager import picker
import matplotlib.pyplot as plt


class SgaMacd:

    def __init__(self):
        self.picker = picker.Picker('1hour')
        candlestick = self.picker.get_candlestick()
        situation = dict()
        situation['short'] = (1, 50)
        situation['long'] = (2, 100)
        situation['signal'] = (1, 50)
        action = dict()
        action['buy'] = (0, 100)
        action['sale'] = (0, 100)
        self.ga = sga.SimpleGeneticAlgorithm(situation, action, 100)
        self.approach = macd.MacD()
        self.approach.setting(candlestick, 13, 26, 9)
        self.data = self.approach.calculate()
        self.data.set_index('time', inplace=True)

    def show_graph(self):
        plt.style.use('ggplot')
        self.data.plot()
        plt.show()


if __name__ == '__main__':
    sga_macd = SgaMacd()
    sga_macd.show_graph()


