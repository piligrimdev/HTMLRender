from UI_Logic import *
import sys
from PyQt5 import QtCore, QtWebEngineWidgets, QtWidgets

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MainWindow()
    myapp.show()
    sys.exit(app.exec_())