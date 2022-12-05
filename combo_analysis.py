import numpy as np
import pandas as pd
from momentumstrategypractice import hqm_dataframe
from valuestrategypractice import rv_dataframe
import sys
import os
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

print('Both strategies include the following stocks as of today:')
for i in hqm_dataframe.index:
    for j in rv_dataframe.index:
        if hqm_dataframe.loc[i, 'Ticker'] == rv_dataframe.loc[j, 'Ticker']:
            print(hqm_dataframe.loc[i, 'Ticker'], '(', 'HQM Ranking:', i+1, 'RV Ranking:', j+1, 'Mean:', ((i+1)+(j+1))/2, ')')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        button = QPushButton("Press Me!")

        self.setMinimumSize(QSize(400, 300))
        self.setMaximumSize(QSize(600, 500))

        # Set the central widget of the Window.
        self.setCentralWidget(button)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

