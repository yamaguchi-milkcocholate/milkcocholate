# milkcocholate

# Modules
```console
cd Jupyter/work/modules
ls
```
- datamanager
- fitnessfunction
- ga
- scheduler

## datamanager
仮想通貨のデータに関する処理を行うクラスが入る

```RealTimeRunner``` : BitBankのAPIをたたいてデータを取り出す。スケジューラにインスタンスを渡すと定期実行できる。
```python
from modules.datamanager import realtimerunner
from modules.scheduler import scheduler

runner = realtimerunner.RealTimeRunner('btc_jpy')
start  = #(開始時刻)
end    = #(終了時刻)
second = #(2回目の実行時刻。3回目以降は等間隔で実行)
# start, end, second はすべてint型の tuple = (year, month, day, hour, minite, second) 

sche = scheduler.Scheduler(runner, start, end, second)
```

```Picker``` : pickleファイルで保存してあるpandas.DataFrameオブジェクトの過去のロウソク足データを取り出す。
```python
from modules.datamanager import picker

candle_type = # '5min' or '15min' or '1hour'
picker = picker.Picker(candle_type)
candlestick =  picker.get_candlestick()
```

```MacD``` : ロウソク足データをもとにMACDとMACDシグナルを計算する
```python
from modules.datamanager import macd

candlestick = # pandas.DataFrame
approach = macd.MacD(candlestick)

# __call__()
# short, long, signal は平滑移動平均線を過去何日にするかを決めるパラメータ
data = approach(short, long, signal)
```

## MACD
![画像](./images/Figure_1.png)

## Line連携
