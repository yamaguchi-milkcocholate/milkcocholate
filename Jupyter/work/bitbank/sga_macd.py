from modules.ga import sga
from modules.datamanager import macd, picker
import matplotlib.pyplot as plt

plt.style.use('ggplot')

picker = picker.Picker('1hour')
candlestick = picker.get_candlestick()

ga = sga.SimpleGeneticAlgorithm([], [], 100)
approach = macd.MacD(candlestick, 13, 26, 9)
data = approach.calculate()
data.set_index('time', inplace=True)
data.plot()
plt.show()
