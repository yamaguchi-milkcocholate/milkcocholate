from modules.ga import sga
from modules.datamanager import macd, picker
import matplotlib.pyplot as plt

# おまじない: 以下を実行するとプロットスタイルが変更されていい感じになる
plt.style.use('ggplot')


picker = picker.Picker('1hour')
candlestick = picker.get_candlestick()

ga = sga.SimpleGeneticAlgorithm([], [], 100)
print(candlestick)
approach = macd.MacD(candlestick, 13, 26, 1, 9)
data = approach.calculate()
data.set_index('time', inplace=True)
data.plot(y=['macd', 'macd_signal'])
plt.show()
