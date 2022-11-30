import numpy as np
import pandas as pd
import xlsxwriter
import requests
from scipy import stats
import math
from secret.APIkey import IEX_CLOUD_API_TOKEN  

stocks = pd.read_csv('sp_500_stocks.csv')

symbol = 'aapl'
api_url = f'https://cloud.iexapis.com/stable/stock/{symbol}/quote?token={IEX_CLOUD_API_TOKEN}'

data = requests.get(api_url)
print(data.status_code)
