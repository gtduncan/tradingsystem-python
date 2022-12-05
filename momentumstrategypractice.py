import numpy as np
import pandas as pd
import requests
import xlsxwriter
import math
from scipy import stats 
from statistics import mean
from secret.APIkey import IEX_CLOUD_API_TOKEN  

# Practice #1

# stocks = pd.read_csv('sp_500_stocks.csv')

# symbol = 'AAPL'
# api_url = f'https://cloud.iexapis.com/stable/stock/{symbol}/quote?token={IEX}'
# data = requests.get(api_url).json()
# price = data['latestPrice']
# market_cap = data['marketCap']

# my_columns = ['Ticker', 'Stock Price', 'Market Capitalization', 'Number of Shares to Buy']


# # for stock in stocks['Ticker'][:5]:
# #     print(stock)
# #     data = requests.get(api_url).json()

# def chunks(lst, n):
#     for i in range(0, len(lst), n):
#         yield lst[i:i + n]

# symbol_groups = list(chunks(stocks['Ticker'], 100))
# symbol_strings = []
# for i in range(0, len(symbol_groups)):
#     symbol_strings.append(','.join(symbol_groups[i]))

# final_dataframe = pd.DataFrame(columns = my_columns)

# for symbol_string in symbol_strings:
#     api_url = f'https://cloud.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=quote,news,chart&token=pk_8d7ed99478374eb288c90d609f8635a4'
#     data = requests.get(api_url).json()
#     for symbol in symbol_string.split(','):
#         new_row = pd.DataFrame(
#         {
#             'Ticker': [symbol],
#             'Stock Price': [data[symbol]['quote']['latestPrice']],
#             'Market Capitalization': [data[symbol]['quote']['marketCap']],
#             'Number of Shares to Buy': 'N/A'
#         },
#         )
#         final_dataframe = pd.concat([final_dataframe, new_row], ignore_index=True)

# portfolio_size = input('Enter the value of your portfolio:')

# try:
#     val = float(portfolio_size)
# except ValueError:
#     print("That's not a number! \n Please try again.")
#     portfolio_size = input('Enter the value of your portfolio:')
#     val = float(portfolio_size)

# position_size = val/len(final_dataframe.index)

# for i in range(0, len(final_dataframe.index)):
#     final_dataframe.loc[i, 'Number of Shares to Buy'] = math.floor(position_size/final_dataframe.loc[i, 'Stock Price'])


# writer.sheets['Recommended Trades'].write('A1', 'Ticker', string_format)
# writer.sheets['Recommended Trades'].write('B1', 'Stock Price', dollar_format)
# writer.sheets['Recommended Trades'].write('C1', 'Market Capitalization', dollar_format)
# writer.sheets['Recommended Trades'].write('D1', 'Number of Shares to Buy', integer_format)

# column_formats = {
#     'A': ['Ticker', string_format],
#     'B': ['Stock Price', dollar_format],
#     'C': ['Market Capitalization', dollar_format],
#     'D': ['Number of Shares to Buy', integer_format]
# }

# for column in column_formats.keys():
#     writer.sheets['Recommended Trades'].set_column(f"{column}:{column}", 18, column_formats[column][1])

# writer.save()

# print(final_dataframe)

stocks = pd.read_csv('sp_500_stocks.csv')

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

symbol_groups = list(chunks(stocks['Ticker'], 100))
symbol_strings = []
for i in range(0, len(symbol_groups)):
    symbol_strings.append(','.join(symbol_groups[i]))

# my_columns = ['Ticker', 'Price', 'One-Year Price Return', 'Number of Shares to Buy']

# final_dataframe = pd.DataFrame(columns=my_columns)

# for symbol_string in symbol_strings:
#     api_url = f"https://cloud.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=stats,price&token={IPX_CLOUD_API_TOKEN}"
#     data = requests.get(api_url).json()
#     for symbol in symbol_string.split(','):
#         new_row = pd.DataFrame(
#         {
#             'Ticker': [symbol],
#             'Price': [data[symbol]['price']],
#             'One-Year Price Return': [data[symbol]['stats']['year1ChangePercent']],
#             'Number of Shares to Buy': 'N/A'
#         },
#         )
#         final_dataframe = pd.concat([final_dataframe, new_row], ignore_index=True)

# final_dataframe.sort_values('One-Year Price Return', ascending=False, inplace=True)
# final_dataframe = final_dataframe[:50]
# final_dataframe.reset_index(inplace=True)

hqm_columns = [
    'Ticker',
    'Price',
    'One-Year Price Return',
    'One-Year Return Percentile',
    'Six-Month Price Return',
    'Six-Month Return Percentile',
    'Three-Month Price Return',
    'Three-Month Return Percentile',
    'One-Month Price Return',
    'One-Month Return Percentile',
    'HQM Score'
]

hqm_dataframe = pd.DataFrame(columns=hqm_columns)

for symbol_string in symbol_strings:
    api_url = f"https://cloud.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=stats,price&token={IEX_CLOUD_API_TOKEN}"
    data = requests.get(api_url).json()
    for symbol in symbol_string.split(','):
        new_row = pd.DataFrame(
        {
            'Ticker': [symbol],
            'Price': [data[symbol]['price']],
            'One-Year Price Return': [data[symbol]['stats']['year1ChangePercent']],
            'One-Year Return Percentile': 'N/A',
            'Six-Month Price Return': [data[symbol]['stats']['month6ChangePercent']],
            'Six-Month Return Percentile': 'N/A',
            'Three-Month Price Return': [data[symbol]['stats']['month3ChangePercent']],
            'Three-Month Return Percentile': 'N/A',
            'One-Month Price Return': [data[symbol]['stats']['month1ChangePercent']],
            'One-Month Return Percentile': 'N/A',
            'HQM Score': 'N/A'
        },
        )
        hqm_dataframe = pd.concat([hqm_dataframe, new_row], ignore_index=True)

time_periods = [
    'One-Year',
    'Six-Month',
    'Three-Month',
    'One-Month'
]

for row in hqm_dataframe.index:
    for time_period in time_periods:
        change_col = f'{time_period} Price Return'
        percentile_col = f'{time_period} Return Percentile'
        hqm_dataframe.loc[row, percentile_col] = stats.percentileofscore(hqm_dataframe[change_col], hqm_dataframe.loc[row, change_col])/100

for row in hqm_dataframe.index:
    momentum_percentiles = []
    for time_period in time_periods:
        momentum_percentiles.append(hqm_dataframe.loc[row, f'{time_period} Return Percentile'])
    hqm_dataframe.loc[row, 'HQM Score'] = mean(momentum_percentiles)

hqm_dataframe.sort_values('HQM Score', ascending=False, inplace=True)
hqm_dataframe = hqm_dataframe[:50]
hqm_dataframe.reset_index(inplace=True, drop=True)

writer = pd.ExcelWriter('momentum_strategy.xlsx', engine = 'xlsxwriter')
hqm_dataframe.to_excel(writer, sheet_name='Momentum Strategy', index = False)

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
    'C': ['One-Year Price Return', percent_format],
    'D': ['One-Year Return Percentile', percent_format],
    'E': ['Six-Month Price Return', percent_format],
    'F': ['Six-Month Return Percentile', percent_format],
    'G': ['Three-Month Price Return', percent_format],
    'H': ['Three-Month Return Percentile', percent_format],
    'I': ['One-Month Price Return', percent_format],
    'J': ['One-Month Return Percentile', percent_format],
    'K': ['HQM Score', percent_format]
}

for column in column_formats.keys():
    writer.sheets['Momentum Strategy'].set_column(f"{column}:{column}", 25, column_formats[column][1])
    writer.sheets['Momentum Strategy'].write(f'{column}1', column_formats[column][0], column_formats[column][1])

writer.save()