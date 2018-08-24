from MainWindow_Design import *
from Render_Design import *
from List_Desing import *

from PyQt5 import QtCore, QtWebEngineWidgets, QtWidgets
from bs4 import BeautifulSoup as bs

from zipfile import ZipFile as zip
import os
import io
import shutil


def Title_Refs(core_dir, opfFile, files):
    with open(opfFile) as opf:
        text = opf.read()
    soup = bs(text)
    list = soup.find_all('item', {'media-type': 'application/xhtml+xml'})
    new_list = []
    for item in list:
        new_list.append(item.get('href'))
    list = new_list
    del new_list
    dict = {}
    titles = {}
    for file in files:
        f = open(core_dir + file, encoding='utf8')
        text = f.read()

        soup = bs(text)
        titles[file] = soup.find('title').text

    for item in list:
        for file in files:
            if item in file:
                dict[core_dir + file] = titles[file]

    print(dict)
    return dict

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow, QtWebEngineWidgets.QWebEngineView):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        self.core_dir = r'C:/Users/User/PycharmProjects/HTMLRender/Books/'
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
            files = []
            try:
                namelist = epub.namelist()
                for name in namelist:
                    epub.extract(name, self.core_dir)
                    if name.endswith('.opf'):
                        opfFile = self.core_dir + name
                    elif name.endswith('html') or name.endswith('xhtml'):
                        files.append(name)

                print(opfFile)
                names = Title_Refs(self.core_dir, opfFile, files)
                self.ListForm.setList(names)
                self.stackedWidget.setCurrentIndex(1)
            except FileNotFoundError as err:
                print("Something gone wrong!")
                print('Error: ', str(err))


class LoadForm(QtWidgets.QDialog, Ui_Dialog, QtWebEngineWidgets.QWebEngineView):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.go_back_page)
        self.pushButton1.clicked.connect(self.go_next_page)
        self.pushButton2.clicked.connect(self.open_list)

    def load(self, u):
        self.url = u
        self.file_view.load(QtCore.QUrl(self.url))

    def setItem(self, it):
        self.item = it

    def setItemsWid(self, wid):
        self.itemwid = wid

    def go_back_page(self):
        try:
            self.itemwid.load_prev(self.item)
        except Exception as e:
            print(e)

    def go_next_page(self):
        self.itemwid.load_next(self.item)

    def open_list(self):
        self.itemwid.setHidden(False)
        self.close()

class List_Files(QtWidgets.QDialog, Ui_Form):
    def __init__(self, namesList = None):
        super().__init__()
        self.setupUi(self)

        self.dict = {}
        self.url = ''
        self.LoadForm = LoadForm()
        self.itemList = {}

        self.listWidget.itemDoubleClicked.connect(self.load)
        if namesList is not None:
            for name in namesList:
                    self.dict[name[1]] = name[0]
                    item = QtWidgets.QListWidgetItem(name[1], self.listWidget)
                    self.listWidget.insertItem(0, item)

    def load(self, item):
        self.LoadForm.setItemsWid(self)
        print(item.text())
        self.url = 'file:///' + self.dict[item.text()]
        self.LoadForm.setItem(item)
        self.LoadForm.load(self.url)
        self.hide()
        self.LoadForm.exec_()
        self.setHidden(False)

    def load_prev(self, item):
            index = self.itemList[item.text()] - 1
            if index >= 0:
                self.listWidget.setCurrentRow(index)
                item_prev = self.listWidget.currentItem()
                print(item_prev.text())
                self.url = 'file:///' + self.dict[item_prev.text()]
                self.LoadForm.setItem(item_prev)
                self.LoadForm.load(self.url)
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setText("There's no more previews pages!")
                mbox.exec_()

    def load_next(self, item):
            index = self.itemList[item.text()] + 1
            if index <= self.pagesCount:
                self.listWidget.setCurrentRow(index)
                item_prev = self.listWidget.currentItem()
                print(item_prev.text())
                self.url = 'file:///' + self.dict[item_prev.text()]
                self.LoadForm.setItem(item_prev)
                self.LoadForm.load(self.url)
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setText("There's no more pages!")
                mbox.exec_()

    def setList(self, namesList):
        count = 0
        for name in namesList:
            self.dict[namesList[name]] = name
            item = QtWidgets.QListWidgetItem(name, self.listWidget)
            item.setText(namesList[name])
            try:
                self.itemList[item.text()] = count
                self.listWidget.insertItem(0, item)
            except Exception as e:
                print(e)
            count += 1
        self.pagesCount = count