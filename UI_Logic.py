from MainWindow_Design import *
from Render_Design import *
from List_Desing import *

from PyQt5 import QtCore, QtWebEngineWidgets, QtWidgets
from bs4 import BeautifulSoup as bs

from zipfile import ZipFile as zip
import os
import io
import shutil

def Title_Refs(files):
    titles = []
    for file in files:
        item = []
        item.append(file)
        file = io.open(file, encoding='utf-8')
        title_soup = bs(file.read())
        title = title_soup.find('title').text
        item.append(title)
        titles.append(item)

    print(titles)
    return  titles

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow, QtWebEngineWidgets.QWebEngineView):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        self.actionOpen.triggered.connect(self.open_loadForm)
        self.file_view.load(QtCore.QUrl('file:///C:/Users/User/PycharmProjects/HTMLRender/MaWinTitle.html'))
        self.ListForm = List_Files()
        self.RenderForm = LoadForm()
        self.stackedWidget.addWidget(self.ListForm)

    def closeEvent(self, event):
        for root, dirs, files in os.walk(self.core_dir):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))

    def open_loadForm(self):
        selectFile = QtWidgets.QFileDialog()

        selectFile.setNameFilter("EBook (*.epub)")
        selectFile.exec_()
        name = selectFile.selectedFiles()
        if name != []:
            epub = zip(name[0])
            self.core_dir = r'C:/Users/User/PycharmProjects/HTMLRender/Books/'
            files = []
            try:
                namelist = epub.namelist()
                for name in namelist:
                    epub.extract(name, self.core_dir)
                    if name.endswith('.opf'):
                        raw_name = name
                        opfFile = 'file:///' + self.core_dir + name
                    elif name.endswith('.html') or name.endswith('xhtml'):
                        files.append(self.core_dir + name)


                print(opfFile)
                names = Title_Refs(files)
                self.ListForm.setList(names)
                self.stackedWidget.setCurrentIndex(1)
            except FileNotFoundError as err:
                print("Something gone wrong!")
                print('Error: ', str(err))


class LoadForm(QtWidgets.QDialog, Ui_Dialog, QtWebEngineWidgets.QWebEngineView):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
    def load(self, u):
        self.url = u
        self.file_view.load(QtCore.QUrl(self.url))


class List_Files(QtWidgets.QDialog, Ui_Form):
    def __init__(self, namesList = None):
        super().__init__()
        self.setupUi(self)

        self.dict = {}
        self.url = ''
        self.LoadForm = LoadForm()

        self.listWidget.itemDoubleClicked.connect(self.load)
        if namesList is not None:
            for name in namesList:
                    self.dict[name[1]] = name[0]
                    item = QtWidgets.QListWidgetItem(name[1], self.listWidget)
                    self.listWidget.insertItem(0, item)

    def load(self, item):
        print(item.text())
        raw_name = self.dict[item.text()]
        self.url = 'file:///' + raw_name
        self.LoadForm.load(self.url)
        self.hide()
        self.LoadForm.exec_()
        self.setHidden(False)

    def setList(self, namesList):
        for name in namesList:
            self.dict[name[1]] = name[0]
            item = QtWidgets.QListWidgetItem(name[1], self.listWidget)
            self.listWidget.insertItem(0, item)