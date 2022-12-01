import numpy as np
import pandas as pd
import xlsxwriter
import requests
from scipy import stats
from statistics import mean
import math
from secret.APIkey import IEX_CLOUD_API_TOKEN  

stocks = pd.read_csv('sp_500_stocks.csv')

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

symbol_groups = list(chunks(stocks['Ticker'], 100))
symbol_strings = []
for i in range(0, len(symbol_groups)):
    symbol_strings.append(','.join(symbol_groups[i]))

# my_columns = ['Ticker', 'Price', 'Price-to-Earnings Ratio', 'Number of Shares to Buy']

# final_dataframe = pd.DataFrame(columns=my_columns)
# final_dataframe

# for symbol_string in symbol_strings:
#     api_url = f"https://cloud.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=quote&token={IEX_CLOUD_API_TOKEN}"
#     data = requests.get(api_url).json()
#     for symbol in symbol_string.split(','):
#         new_row = pd.DataFrame({
#             'Ticker': [symbol],
#             'Price': [data[symbol]['quote']['latestPrice']],
#             'Price-to-Earnings Ratio': [data[symbol]['quote']['peRatio']],
#             'Number of Shares to Buy': 'N/A'
#         })
#         final_dataframe = pd.concat([final_dataframe, new_row], ignore_index=True)

# final_dataframe.sort_values('Price-to-Earnings Ratio', inplace=True)
# final_dataframe= final_dataframe[final_dataframe['Price-to-Earnings Ratio'] > 0]
# final_dataframe = final_dataframe[:50]
# final_dataframe.reset_index(inplace=True, drop=True)

def portfolio_input():
    global portfolio_size
    portfolio_size = input('Enter the value of your portfolio:')
    try:
        float(portfolio_size)
    except ValueError:
        print("That's not a number! \n Please try again.")
        portfolio_size = input('Enter the value of your portfolio:')


# print(final_dataframe)

# Price-to-earnings ratio

# pe_ratio = data[symbol]['quote']['peRatio']

# # Price-to-book ratio

# pb_ratio = data[symbol]['advanced-stats']['priceToBook']

# # Price-to-sales ratio

# ps_ratio = data[symbol]['advanced-stats']['priceToSales']

# # Enterprise Value divided by Earnings Before Interest, Taxes, Depreciation, and Amortization (EV/EBITDA)

# enterprise_value = data[symbol]['advanced-stats']['enterpriseValue']
# ebitda = data[symbol]['advanced-stats']['EBITDA']
# ev_to_ebitda = enterprise_value/ebitda

# # Enterprise Value divided by Gross Profit (EV/GP)
# gross_profit = data[symbol]['advanced-stats']['grossProfit']
# ev_to_gross_profit = enterprise_value/gross_profit

rv_columns = [
    'Ticker',
    'Price',
    'Number of Shares to Buy',
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
            'Number of Shares to Buy': 'N/A',
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

for column in ['Price-to-Earnings Ratio', 'Price-to-Book Ratio', 'Price-to-Sales Ratio', 'EV/EBITDA', 'EV/GP']:
    rv_dataframe[column].fillna(rv_dataframe[column].mean(), inplace=True)

print(rv_dataframe)

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
rv_dataframe = rv_dataframe[:50]
rv_dataframe.reset_index(inplace=True, drop=True)

portfolio_input()

position_size = float(portfolio_size)/len(rv_dataframe.index)

for row in rv_dataframe.index:
    rv_dataframe.loc[row, 'Number of Shares to Buy'] = math.floor(position_size/rv_dataframe.loc[row, 'Price'])

print(rv_dataframe)

writer = pd.ExcelWriter('value_strategy.xlsx', engine='xlsxwriter')
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
    'C': ['Number of Shares to Buy', integer_format],
    'D': ['Price-to-Earnings Ratio', float_format],
    'E': ['PE Percentile', percent_format],
    'F': ['Price-to-Book Ratio', float_format],
    'G': ['PB Percentile', percent_format],
    'H': ['Price-to-Sales Ratio', float_format],
    'I': ['PS Percentile', percent_format],
    'J': ['EV/EDITBA', float_format],
    'K': ['EV/EDITBA Percentile', percent_format],
    'L': ['EV/GP', float_format],
    'M': ['EV/GP Percentile', percent_format],
    'N': ['RV Score', percent_format]
}

for column in column_formats.keys():
    writer.sheets['Value Strategy'].set_column(f"{column}:{column}", 25, column_formats[column][1])
    writer.sheets['Value Strategy'].write(f'{column}1', column_formats[column][0], column_formats[column][1])

writer.save()