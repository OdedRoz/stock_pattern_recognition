import numpy as np
import pandas as pd
import math

class window:
    weights = {0: [0.5, 1, 1, 0.5, 0, 0, -0.5, -0.5, -1, -1],
               1: [0, 0.5, 1, 1, 0.5, 0, 0, -1, -1, -1],
               2: [-1, 0, 0.5, 1, 1, 0.5, 0, 0, -1, -1],
               3: [-1, -0.5, 0, 0.5, 1, 1, 0.5, 0, -0.5, -1],
               4: [-1, -1, -0.5, 0, 0.5, 1, 1, 0.5, 0, -1],
               5: [-1, -1, -0.5, -0.5, 0, 0.5, 1, 1, 0.5, 0],
               6: [-1, -1, -0.5, -0.5, 0, 0, 0.5, 1, 1, 0.5],
               7: [-1, -1, -0.5, -0.5, 0, 0, 0.5, 1, 1, 0.5],
               8: [-1, -0.5, 0, 0, 0.5, 1, 1, 1, 0, -2],
               9: [0, 0, 0.5, 1, 1, 1, 1, 0, -0.2, -2.5]
               }
    weights_matrix = pd.DataFrame(data=weights)

    def __init__(self,data):
        self.data = data
        self.data_len = len(data)
        self.min_value = data['CLOSE'].min()
        self.max_value = data['CLOSE'].max()
        #self.value_step = ((self.max_value-self.min_value)/10)
        self.matrix_rows_valus = np.linspace(self.min_value,self.max_value, num=10)
        self.candles_in_coulmn = math.ceil(len(data)/10)
        self.value_to_add = 1/self.candles_in_coulmn
        self.matrix = self.create_matrix()
        self.reversed_matrix = self.matrix.iloc[::1]
        self.fitting_score = self.get_fitting_score()



    def create_matrix(self):
        matrix = pd.DataFrame(index=self.matrix_rows_valus,columns=range(10))
        current_coulmn = 0
        for i in range(0,self.data_len,self.candles_in_coulmn):
            matrix[current_coulmn] = 0
            chunk = self.data[i:i+self.candles_in_coulmn]
            rows = np.digitize(chunk['CLOSE'], self.matrix_rows_valus)
            for row in rows:
                matrix.iloc[row-1,current_coulmn] += self.value_to_add
            current_coulmn += 1
        return matrix

    def get_fitting_score(self):
        return self.reversed_matrix.reset_index(drop=True).mul(self.weights_matrix).values.sum()




