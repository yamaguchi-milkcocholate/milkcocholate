import pandas as pd


def simple_moving_average(candlestick_end, term):
    """
    ロウソク足データの終値から単純移動平均線を計算してDataFrameで返す
    :param: candlestick_end pandas.DataFrame
    :param: term            integer
    :return:
    """
    if not ('end' in candlestick_end.columns.values):
        raise TypeError('column "end" not found')
    average_list = list()
    # 開始位置
    start = term - 1
    # ループ回数 = 返すDataFrameの行数
    iteration = len(candlestick_end) - start
    for i in range(iteration):
        part = candlestick_end.loc[i:start + i]
        end_sum = 0
        for index, row in part.iterrows():
            end_sum += int(row['end'])
        average_list.append(float(end_sum / term))
    return pd.DataFrame(data=average_list, columns=['simple_moving_average'])


def exponential_moving_average(candlestick_end, term):
    """
    ロウソク足データの終値から指数移動平均線を計算してDataFrameで返す
    :param: candlestick_end pandas.DataFrame
    :param: term            integer
    :return:
    """
    if not ('end' in candlestick_end.columns.values):
        raise TypeError('column "end" not found')
    alpha = float(2 / (term + 1))
    average_list = list()
    # 開始位置
    start = term - 1
    # ループ回数 = 返すDataFrameの行数
    iteration = len(candlestick_end) - start
    # 最初の1回は単純移動平均
    part = candlestick_end.loc[0:start]
    end_sum = 0
    for index, row in part.iterrows():
        end_sum += int(row['end'])
    average_list.append(float(end_sum / term))
    # 2回目以降
    for i in range(start + 1, len(candlestick_end)):
        part = candlestick_end.loc[i, 'end']
        pre = average_list[-1]
        average_list.append(float(pre + alpha * (part - pre)))
    return pd.DataFrame(data=average_list, columns=['exponential_moving_average'])
