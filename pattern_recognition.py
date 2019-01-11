from get_intraday_stock_data import get_quote_data
from window import window
import math
import pandas as pd
import numpy as np




def pattern_recognition(Tik,data_range,data_interval,fitting_window_range,keep_window,minimum_score_to_buy):
    data = get_quote_data(Tik,data_range,data_interval)
    fitting_window_rows_len = get_fitting_window_rows_len(data_interval,fitting_window_range)
    data_len = len(data)
    print(f'crateing {data_len-fitting_window_rows_len} windows matrixes')
    windoes = []
    fitting_values = []
    for idx in range(data_len):
        if idx+fitting_window_rows_len <= data_len:
            windoes.append(window(data.iloc[idx:idx+fitting_window_rows_len]))
            fitting_values.append(windoes[idx].fitting_score)
            if idx%50 == 0:
                print(f'created {idx} matrixes')
    buy_times = find_buy_times(fitting_values,windoes,minimum_score_to_buy)
    calc_profit(data,buy_times,keep_window,data_interval)


def find_buy_times(fitting_values,windoes,minimum_score_to_buy):
    array = np.array(fitting_values)
    top_n_index = np.argsort(array)[:]
    buy_indexes = []
    used_dates = []
    for i in reversed(top_n_index):
        print('score: ' + str(windoes[i].fitting_score))
        print('buy time: ' + (str(windoes[i].data.iloc[-1:].index.values)))
        print('price: ' + str(windoes[i].data.iloc[-1:]['CLOSE'].values))
        print('-'*20)
        if windoes[i].fitting_score >= minimum_score_to_buy:
            timeindex = windoes[i].data.iloc[-1:].index
            if (timeindex.date,timeindex.hour) not in used_dates:
                buy_indexes.append(timeindex)
                used_dates.extend(((timeindex.date,timeindex.hour),(timeindex.date,timeindex.hour+1),(timeindex.date,timeindex.hour-1)))
        else:
            break
    return buy_indexes




def calc_profit(data,buy_times,keep_window,data_interval):
    if keep_window[-1] != 'm':
        print('keep_window which is not in minutes is not supported yet')
        raise ValueError
    total_revenue = 0
    for buy_index in buy_times:
        sell_index = buy_index + pd.DateOffset(minutes=float(keep_window[:-1]))
        buy_price = data.loc[buy_index]['CLOSE'][0]
        sell_price = data.loc[sell_index]['CLOSE'][0]
        revenue = sell_price - buy_price
        print('time: ' + str(buy_index[0]))
        print('buy price: ' + str(buy_price) + ' sell price: ' + str(sell_price))
        print('revenue: ' +str(revenue))
        print('-'*20)
        total_revenue += revenue
    print('/n' +'total revenue is: ' + str(total_revenue))









def get_fitting_window_rows_len(data_interval,window_range):
    if data_interval[-1] != window_range[-1]:
        print('fitting_window_range time kind should be the same as data_interval (m/h/d)')
        raise ValueError
    else:
        window_range_mum = float(window_range[:-1])
        data_interval_num = float(data_interval[:-1])
        return math.ceil(window_range_mum/data_interval_num)


if __name__ == '__main__':
    Tik = 'CRON'
    data_range = '30d'
    data_interval = '5m'
    #fitting_window_range time kind should be the same as data_interval (m/h/d)
    fitting_window_range = '240m'
    minimum_score_to_buy = 7.0
    #must be complete multiply of data_interval
    keep_window = '30m'
    pattern_recognition(Tik,data_range,data_interval,fitting_window_range,keep_window,minimum_score_to_buy)



