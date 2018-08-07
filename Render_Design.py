from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets


class Ui_Dialog(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Load")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.file_view = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        self.file_view.setGeometry(QtCore.QRect(0, 0, 800, 550))
        self.file_view.setObjectName("widget")
        self.pushButton = QtWidgets.QPushButton(MainWindow)
        self.pushButton.setGeometry(QtCore.QRect(10, 560, 75, 23))
        self.pushButton.setObjectName("pushButton")
        #MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Booker", "Booker"))
        self.pushButton.setText(_translate("Dialog", "Back"))
