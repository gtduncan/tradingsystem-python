import numpy as np
import pandas as pd
from momentumstrategypractice import hqm_dataframe
from valuestrategypractice import rv_dataframe

print('Both strategies include the following stocks as of today:')
for i in hqm_dataframe.index:
    for j in rv_dataframe.index:
        if hqm_dataframe.loc[i, 'Ticker'] == rv_dataframe.loc[j, 'Ticker']:
            print(hqm_dataframe.loc[i, 'Ticker'], '(', 'HQM Ranking:', i+1, 'RV Ranking:', j+1, ')')