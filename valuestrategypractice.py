import numpy as np
import pandas as pd
import xlsxwriter
import requests
from scipy import stats
from statistics import mean
import math
from secret.APIkey import IEX_CLOUD_API_TOKEN 

stocks = pd.read_csv('NASDAQ.csv')

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

symbol_groups = list(chunks(stocks['Ticker'], 100))
symbol_strings = []
for i in range(0, len(symbol_groups)):
    symbol_strings.append(','.join(symbol_groups[i]))

rv_columns = [
    'Ticker',
    'Price',
    'Price-to-Earnings Ratio',
    'PE Percentile',
    'Price-to-Book Ratio',
    'PB Percentile',
    'Price-to-Sales Ratio',
    'PS Percentile',
    'EV/EBITDA',
    'EV/EBITDA Percentile',
    'EV/GP',
    'EV/GP Percentile',
    'RV Score'
]

rv_dataframe = pd.DataFrame(columns=rv_columns)

for symbol_string in symbol_strings:
    api_url = f"https://cloud.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=quote,advanced-stats&token={IEX_CLOUD_API_TOKEN}"
    data = requests.get(api_url).json()
    for symbol in symbol_string.split(','):
        try:
            enterprise_value = data[symbol]['advanced-stats']['enterpriseValue']
            ebitda = data[symbol]['advanced-stats']['EBITDA']
            gross_profit = data[symbol]['advanced-stats']['grossProfit']
            try:
                ev_to_ebitda = enterprise_value/ebitda
            except TypeError:
                ev_to_ebitda = np.NaN
            try:
                ev_to_gross_profit = enterprise_value/gross_profit
            except TypeError:
                ev_to_gross_profit = np.NaN
            new_row = pd.DataFrame({
                'Ticker': [symbol],
                'Price': [data[symbol]['quote']['latestPrice']],
                'Price-to-Earnings Ratio': [data[symbol]['quote']['peRatio']],
                'PE Percentile': 'N/A',
                'Price-to-Book Ratio': data[symbol]['advanced-stats']['priceToBook'],
                'PB Percentile': 'N/A',
                'Price-to-Sales Ratio': data[symbol]['advanced-stats']['priceToSales'],
                'PS Percentile': 'N/A',
                'EV/EBITDA': ev_to_ebitda,
                'EV/EBITDA Percentile': 'N/A',
                'EV/GP': ev_to_gross_profit,
                'EV/GP Percentile': 'N/A',
                'RV Score': 'N/A'
            })
            rv_dataframe = pd.concat([rv_dataframe, new_row], ignore_index=True)
        except:
            print('Could not access', symbol)

for column in ['Price-to-Earnings Ratio', 'Price-to-Book Ratio', 'Price-to-Sales Ratio', 'EV/EBITDA', 'EV/GP']:
    rv_dataframe[column].fillna(rv_dataframe[column].mean(), inplace=True)

rv_dataframe.dropna(subset='Price', inplace=True)

metrics= {
    'Price-to-Earnings Ratio': 'PE Percentile',
    'Price-to-Book Ratio' : 'PB Percentile',
    'Price-to-Sales Ratio' : 'PS Percentile',
    'EV/EBITDA' : 'EV/EBITDA Percentile',
    'EV/GP' :'EV/GP Percentile',
}

for metric in metrics.keys():
    for row in rv_dataframe.index:
        rv_dataframe.loc[row, metrics[metric]] = stats.percentileofscore(rv_dataframe[metric], rv_dataframe.loc[row, metric])/100

for row in rv_dataframe.index:
    value_percentiles = []
    for metric in metrics.keys():
        value_percentiles.append(rv_dataframe.loc[row, metrics[metric]])
    rv_dataframe.loc[row, 'RV Score'] = mean(value_percentiles)

rv_dataframe.sort_values('RV Score', ascending=True, inplace=True)
rv_dataframe = rv_dataframe[:500]
rv_dataframe.reset_index(inplace=True, drop=True)

writer = pd.ExcelWriter('excel/value_strategy.xlsx', engine='xlsxwriter')
rv_dataframe.to_excel(writer, sheet_name='Value Strategy', index=False)

background_color = '#ffffff'
font_color = '#000000'

string_format = writer.book.add_format(
    {
        "font_color": font_color,
        "bg_color": background_color,
        "border": 1
    }
)

dollar_format = writer.book.add_format(
    {
        "num_format": '$0.00',
        "font_color": font_color,
        "bg_color": background_color,
        "border": 1
    }
)

integer_format = writer.book.add_format(
    {
        "num_format": '0',
        "font_color": font_color,
        "bg_color": background_color,
        "border": 1
    }
)

float_format = writer.book.add_format(
    {
        "num_format": '0.00',
        "font_color": font_color,
        "bg_color": background_color,
        "border": 1
    }
)

percent_format = writer.book.add_format(
    {
        "num_format": '0.0%',
        "font_color": font_color,
        "bg_color": background_color,
        "border": 1
    }
)

column_formats = {
    'A': ['Ticker', string_format],
    'B': ['Price', dollar_format],
    'C': ['Price-to-Earnings Ratio', float_format],
    'D': ['PE Percentile', percent_format],
    'E': ['Price-to-Book Ratio', float_format],
    'F': ['PB Percentile', percent_format],
    'G': ['Price-to-Sales Ratio', float_format],
    'H': ['PS Percentile', percent_format],
    'I': ['EV/EDITBA', float_format],
    'J': ['EV/EDITBA Percentile', percent_format],
    'K': ['EV/GP', float_format],
    'L': ['EV/GP Percentile', percent_format],
    'M': ['RV Score', percent_format]
}

for column in column_formats.keys():
    writer.sheets['Value Strategy'].set_column(f"{column}:{column}", 25, column_formats[column][1])
    writer.sheets['Value Strategy'].write(f'{column}1', column_formats[column][0], column_formats[column][1])

writer.save()