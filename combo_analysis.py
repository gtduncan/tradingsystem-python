import numpy as np
import pandas as pd
from momentumstrategypractice import hqm_dataframe
from valuestrategypractice import rv_dataframe
import sys
import os
from random import choice, randint
from PyQt6 import QtWidgets, QtCore, QtGui, uic
from ui.ui_trading_ui import Ui_StockTracker

combo_columns = [
    'Ticker',
    'Price',
    'HQM Ranking',
    'RV Ranking',
    'Mean Ranking'
]

combo_dataframe = pd.DataFrame(columns=combo_columns)

for i in hqm_dataframe.index:
    for j in rv_dataframe.index:
        if hqm_dataframe.loc[i, 'Ticker'] == rv_dataframe.loc[j, 'Ticker']:
            new_row = pd.DataFrame(
                {
                    'Ticker': [hqm_dataframe.loc[i, 'Ticker']] ,
                    'Price': [hqm_dataframe.loc[i, 'Price']] ,
                    'HQM Ranking': [i],
                    'RV Ranking': [j],
                    'Mean Ranking': [(((i+1)+(j+1))/2)]
                }, )
            combo_dataframe = pd.concat([combo_dataframe, new_row], ignore_index=True)

print(combo_dataframe)

class MainWindow(QtWidgets.QWidget, Ui_StockTracker):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle('Stock Tracker')
        self.stockInfo.setReadOnly(True)
        self.run.clicked.connect(self.button_clicked)
    def button_clicked(self):
        self.stockInfo.clear()
        self.stockInfo.insertHtml('Both value-based and momentum-based strategies include the following stocks as of today: <br><br>')
        for i in hqm_dataframe.index:
            for j in rv_dataframe.index:
                if hqm_dataframe.loc[i, 'Ticker'] == rv_dataframe.loc[j, 'Ticker']:
                    self.stockInfo.insertHtml(str(hqm_dataframe.loc[i, 'Ticker']))
                    self.stockInfo.insertHtml(': (HQM Ranking: ')
                    self.stockInfo.insertHtml(str(i+1))
                    self.stockInfo.insertHtml(', RV Ranking: ')
                    self.stockInfo.insertHtml(str(j+1))
                    self.stockInfo.insertHtml(', Mean: ')
                    self.stockInfo.insertHtml(str(((i+1)+(j+1))/2))
                    self.stockInfo.insertHtml(') <br>')
                    # '(', 'HQM Ranking:', i+1, 'RV Ranking:', j+1, 'Mean:', ((i+1)+(j+1))/2, ')')
    
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
