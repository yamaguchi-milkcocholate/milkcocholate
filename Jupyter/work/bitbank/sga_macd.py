from modules.ga import sga
from modules.datamanager import macd
import matplotlib.pyplot as plt


class SgaMacd:
    DEFAULT_STEPS = 10000

    def __init__(self):
        situation = list()
        situation.append((1, 50))
        situation.append((2, 100))
        situation.append((1, 50))
        self.ga = sga.SimpleGeneticAlgorithm(situation, population=2)

    def back_test(self, steps=DEFAULT_STEPS):
        self.ga(steps)

    def show_graph(self):
        pass
        #plt.style.use('ggplot')
        #self.data.plot()
        #plt.show()


if __name__ == '__main__':
    sga_macd = SgaMacd()
    sga_macd.back_test(10)
    sga_macd.ga.init_population()
    #sga_macd.show_graph()


