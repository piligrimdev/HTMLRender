from MainWindow_Design import *
from Render_Design import *
from PyQt5 import QtCore, QtWebEngineWidgets, QtWidgets


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow, QtWebEngineWidgets.QWebEngineView):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        self.actionOpen.triggered.connect(self.open_loadForm)
        self.file_view.load(QtCore.QUrl('file:///C:/Users/User/PycharmProjects/HTMLRender/MaWinTitle.html'))

    def open_loadForm(self):
        selectFile = QtWidgets.QFileDialog()

        selectFile.setNameFilter("HTML (*.html *.xhtml *.htm)")
        selectFile.exec_()
        name = selectFile.selectedUrls()
        if name != []:
            name = str(name)
            name = name.replace("[PyQt5.QtCore.QUrl('", "")
            name = name.replace("')]", "")
            load_form = LoadForm(name)
            load_form.exec_()


class LoadForm(QtWidgets.QDialog, Ui_Dialog, QtWebEngineWidgets.QWebEngineView):
    def __init__(self, openUrl = None):
        super().__init__()
        self.setupUi(self)
        if openUrl is None:
            self.file_view.load(QtCore.QUrl('https://www.google.com/'))
        else:
            self.file_view.load(QtCore.QUrl(openUrl))

    def load(self):
        url = self.lineEdit.text()
        self.widget.load(QtCore.QUrl(url))