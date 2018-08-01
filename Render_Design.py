from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets


class Ui_Dialog(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Load")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.file_view = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        self.file_view.setGeometry(QtCore.QRect(0, 39, 801, 511))
        self.file_view.setObjectName("widget")
        #MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Booker", "Booker"))