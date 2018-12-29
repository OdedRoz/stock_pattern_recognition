from get_intraday_stock_data import get_quote_data
from window import window
import math
import pandas as pd




def pattern_recognition(Tik,data_range,data_interval,fitting_window_range):
    data = get_quote_data(Tik,data_range,data_interval)
    fitting_window_rows_len = get_fitting_window_rows_len(data_interval,fitting_window_range)
    data_len = len(data)
    print(f'crateing {data_len-fitting_window_rows_len} windows matrixes')
    windoes = []
    fitting_values = []
    for idx in range(data_len):
        if idx+fitting_window_rows_len <= data_len:
            windoes.append(window(data[idx:idx+fitting_window_rows_len]))
            fitting_values.append(windoes[idx].fitting_score)
            if idx%50 == 0:
                print(f'created {idx} matrixes')
    pass



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
    data_range = '1d'
    data_interval = '1m'
    #fitting_window_range time kind should be the same as data_interval (m/h/d)
    fitting_window_range = '60m'
    pattern_recognition(Tik,data_range,data_interval,fitting_window_range)



