import numpy as np
import pandas as pd
import requests
import xlsxwriter
import math
from scipy import stats 

# Practice #1

# stocks = pd.read_csv('sp_500_stocks.csv')

# symbol = 'AAPL'
# api_url = f'https://cloud.iexapis.com/stable/stock/{symbol}/quote?token=pk_8d7ed99478374eb288c90d609f8635a4'
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

# writer = pd.ExcelWriter('recommended trades.xlsx', engine = 'xlsxwriter')
# final_dataframe.to_excel(writer, 'Recommended Trades', index = False)

# background_color = '#ffffff'
# font_color = '#000000'

# string_format = writer.book.add_format(
#     {
#         "font_color": font_color,
#         "bg_color": background_color,
#         "border": 1
#     }
# )

# dollar_format = writer.book.add_format(
#     {
#         "num_format": '$0.00',
#         "font_color": font_color,
#         "bg_color": background_color,
#         "border": 1
#     }
# )

# integer_format = writer.book.add_format(
#     {
#         "num_format": '0',
#         "font_color": font_color,
#         "bg_color": background_color,
#         "border": 1
#     }
# )

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

IPX_CLOUD_API_TOKEN = 'pk_8d7ed99478374eb288c90d609f8635a4'

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

symbol_groups = list(chunks(stocks['Ticker'], 100))
symbol_strings = []
for i in range(0, len(symbol_groups)):
    symbol_strings.append(','.join(symbol_groups[i]))

my_columns = ['Ticker', 'Price', 'One-Year Price Return', 'Number of Shares to Buy']

final_dataframe = pd.DataFrame(columns=my_columns)

for symbol_string in symbol_strings:
    api_url = f"https://cloud.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=stats,price&token={IPX_CLOUD_API_TOKEN}"
    data = requests.get(api_url).json()
    for symbol in symbol_string.split(','):
        new_row = pd.DataFrame(
        {
            'Ticker': [symbol],
            'Price': [data[symbol]['price']],
            'One-Year Price Return': [data[symbol]['stats']['year1ChangePercent']],
            'Number of Shares to Buy': 'N/A'
        },
        )
        final_dataframe = pd.concat([final_dataframe, new_row], ignore_index=True)

final_dataframe.sort_values('One-Year Price Return', ascending=False, inplace=True)
final_dataframe = final_dataframe[:50]
final_dataframe.reset_index(inplace=True)

def portfolio_input():
    global portfolio_size
    portfolio_size = input('Enter the value of your portfolio:')
    try:
        float(portfolio_size)
    except ValueError:
        print("That's not a number! \n Please try again.")
        portfolio_size = input('Enter the value of your portfolio:')

portfolio_input()

position_size = float(portfolio_size)/len(final_dataframe.index)
for i in range(0, len(final_dataframe.index)):
    final_dataframe.loc[i, 'Number of Shares to Buy'] = math.floor(position_size/final_dataframe.loc[i, 'Price'])

print(position_size)

print(final_dataframe)