# Form implementation generated from reading ui file '/Users/georgeduncan/Projects/tradingsystem-python/trading_ui.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_StockTracker(object):
    def setupUi(self, StockTracker):
        StockTracker.setObjectName("StockTracker")
        StockTracker.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(StockTracker)
        self.gridLayout.setObjectName("gridLayout")
        self.run = QtWidgets.QPushButton(StockTracker)
        self.run.setObjectName("run")
        self.gridLayout.addWidget(self.run, 1, 0, 1, 1)
        self.stockInfo = QtWidgets.QTextEdit(StockTracker)
        self.stockInfo.setObjectName("stockInfo")
        self.gridLayout.addWidget(self.stockInfo, 0, 0, 1, 1)

        self.retranslateUi(StockTracker)
        QtCore.QMetaObject.connectSlotsByName(StockTracker)

    def retranslateUi(self, StockTracker):
        _translate = QtCore.QCoreApplication.translate
        StockTracker.setWindowTitle(_translate("StockTracker", "Form"))
        self.run.setText(_translate("StockTracker", "Run"))