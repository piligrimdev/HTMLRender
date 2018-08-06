from MainWindow_Design import *
from Render_Design import *
from List_Desing import *

from PyQt5 import QtCore, QtWebEngineWidgets, QtWidgets
from bs4 import BeautifulSoup as bs

from zipfile import ZipFile as zip
import os
import io
import shutil

def Title_Refs(dir, opfFile):
    with open(str(dir + opfFile)) as file:
        opfInfo = file.read()
    soup = bs(opfInfo)
    list = []
    refs = soup.find_all('item', {'media-type': 'application/xhtml+xml'})
    for item in refs:
        list.append(item.get('href'))

    titles = []
    for item in list:
        path = dir + item
        item = []
        item.append(path)
        file = io.open(path, encoding='utf-8')
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

    def open_loadForm(self):
        selectFile = QtWidgets.QFileDialog()

        selectFile.setNameFilter("EBook (*.epub)")
        selectFile.exec_()
        name = selectFile.selectedFiles()
        if name != []:
            epub = zip(name[0])
            core_dir = r'C:/Users/User/PycharmProjects/HTMLRender/Books/'
            try:
                namelist = epub.namelist()
                for name in namelist:
                    epub.extract(name, core_dir)
                    if name.endswith('.opf'):
                        raw_name = name
                        opfFile = 'file:///' + core_dir + name

                names = Title_Refs(core_dir, raw_name)
                print(opfFile)
                lw = List_Files(names)
                lw.setModal(True)
                self.hide()
                lw.exec_()
                self.setHidden(False)
            except FileNotFoundError:
                print("Something gone wrong!")
            finally:
                for root, dirs, files in os.walk(core_dir):
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))


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


class List_Files(QtWidgets.QDialog, Ui_Form):
    def __init__(self, namesList):
        super().__init__()
        self.setupUi(self)
        self.dict = {}
        self.listWidget.itemDoubleClicked.connect(self.load)
        for name in namesList:
                self.dict[name[1]] = name[0]
                item = QtWidgets.QListWidgetItem(name[1], self.listWidget)
                self.listWidget.insertItem(0, item)

    def load(self, item):
        print(item.text())
        raw_name = self.dict[item.text()]
        url = 'file:///' + raw_name
        self.hide()
        ld = LoadForm(url)
        ld.exec_()
        self.exec_()
