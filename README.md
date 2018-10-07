# milkcocholate

[Docker Hub](https://hub.docker.com/u/milkchocolate22/)

# Docker
flask_web_app
```console
cd Flask_Web_App
docker build -t milkchocolate22/flask_web_app:latest .
(or 'docker pull milkchocolate22/flask_web_app:latest')
docker run -d -v $PWD:/home/app -p 5000:5000 --restart=always --name "FlaskWebApp" milkchocolate22/flask_web_app
```

jupyter
```console
cd Jupyter
docker build -t milkchocolate22/jupyter:latest .
(or 'docker pull milkchocolate22/jupyter:latest')
docker run -d --rm -v $PWD:/home/jovyan/work -p 8888:8888 --name "Jupyter" milkchocolate22/jupyter
```

bitbank
```console
cd BitBank
docker build -t milkchocolate22/bitbank:latest .
(or 'docker pull milkchocolate22/bitbank:latest')
docker run -d -v $PWD:/home/bitbank -p 10080:10080 --restart=always --name "BitBank" milkchocolate22/bitbank
```


# Modules

```console
cd Jupyter/work/modules
ls

# datamanager
# fitnessfunction
# ga
# scheduler
```


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

## fitnessfunction

適応度の計算処理をするクラス。計算にはテクニカル分析が必要であるので、そのクラスのインスタンスを持つ。(MacDクラスなど)

遺伝的アルゴリズムのクラス(SimpleGeneticAlgorithmクラスなど)にインスタンスを持たせて、GeneticAlgorithmクラス内でcalc_fitness()メソッドを呼ぶ。

```SimpleMacDParams``` : MacDの計算に使う「短期」、「長期」、「シグナル」のパラメータを最適化するときの適応度を計算するクラス。

fitnessfunction のクラスはSimpleMacDParamsクラスの実装の仕方を参考に作るとよい。

```python
# GeneticAlgorithmクラスの clac_fitness()メソッドにインスタンスを渡す。
from modules.fitnessfunction import simple_macd_params

candle_type = # '5min' or '15min' or '1hour'
fitness_function = simple_macd_params.SimpleMacDParams(candle_type)

...

def calc_fitness(geno_type, fitness_function):
    fitness = fitness_function.calc_fitness(geno_type)
    return fitness
```

## ga

```GeneticAlgorithm``` : 基本的に遺伝的アルゴリズムがもつメソッドを持つクラス。

GeneticAlgorithmクラスを継承する形より、SGAなどの遺伝的アルゴリズムの派生クラスがGeneticAlgorithmクラスのインスタンスを持つような実装が好ましい。

これは「継承より集約  = is-a-kind-of より has-a 」のデザインパターンから取り入れた。

以降追加されるであろう遺伝的アルゴリズムのクラスはGeneticAlgorithmクラスのメソッドを呼び出すことで、テストの際に引数のチェックや独自に持つメソッドのチェックだけで済むという恩恵がある。(依存関係があるともいえるが...。)

GeneticAlgorithmクラスが持つ遺伝的アルゴリズムの基本的なメソッド

| メソッド | 処理 | 戻り値 |
|:------------:|:---------------:|:------------------------:|
| init_population() | situationをもとにランダムに値を入れる。geno_typeの初期化。 |  |
| generation(step, geno_type, fitness_function, selected_ga) | 進化 | geno_type, fitness |
| selecte_elite(geno_type, fitness) | 優秀な個体を残す | elites |

```python
# GeneticAlgorithmクラス
from module.ga import ga

situation = [(1, 50), (1, 100), (1, 50)]
# 最適化するパラメータが3つ。それぞれの範囲は'1~50', '1~100', 1~50'ということ。

genetic_algorithm = ga.GeneticAlgorithm(mutation=2, cross=70, situation=situation, elite_num=1, population=100)
```

``` SimpleGeneticAlgorithm``` : SGAのクラス

遺伝的アルゴリズムの派生クラスをつくる時にこのクラスのような実装にするとよい。

遺伝子の初期化(init_populationメソッド), 世代交代(generationメソッド)はGeneticAlgorithmクラスに処理を任せる。

独自のメソッドは、determine_next_generation()。例えば、SGAの場合では一点交叉の処理を書く。

```python
from module.ga import sga
from module.ga import ga 

...

  def __init__(...):
    ...
    self.ga = ga.GeneticAlgorithm(...)  # インスタンスをつくる。(継承より集約 = is-a-kind-of より has-a)
    
  def init_population():
    self.geno_type = self.ga.init_population()  # 処理はGeneticAlgorithmクラスを利用
  
  def generation():
    self.geno_type, self.fitness = self.ga.generation(steps, self.geno_type, self.fitness_function, selected_ga=self) 
    # selected_gaには自らのインスタンスを渡す。この場合SGAを選択したことになる。
    # また、GAである必要条件は独自の交叉方法を持つこと。 =  determine_next_generationメソッドを持つこととなる。
    # これは依存関係を生んでしまうので良いのか悪いのか

```

## scheduler

```Scheduler``` : 定期実行の設定を行うクラス

定期実行で行う処理は、○○Runnerクラスのprocessingメソッド。

Schedulerには、
1. Runnerクラスのインスタンス
2. 開始時刻
3. 終了時刻
4. 2回目の実行時刻

を渡し、3回目以降の実行は等間隔に行う。

```python
# 引数を準備
runner = realtimerunner.RealTimeRunner('btc_jpy')
now = datetime.datetime.now()
start = (now.year, now.month, now.day, now.hour, 30, 0)
end = (now.year, now.month, now.day, now.hour + 1, 30, 0)
second = (now.year, now.month, now.day, now.hour, 35, 0)

# インスタンス化
sche = scheduler.Scheduler(runner, start, end, second)

# 定期実行開始　戻り値は引数に渡したrunner
# runnerがプロパティなどにデータを持てば、受け取れる
runner = shce()  

# 実行終了
# データを参照
runner.show_ticker_list()
runner.show_depth_list()

```

## MACD
![画像](./images/Figure_1.png)

## Line連携
