from PyQt5.QtWidgets import (QMainWindow, QApplication, QLabel, QCheckBox,
                             QComboBox, QListWidget, QLineEdit, QLineEdit,
                             QSpinBox, QDoubleSpinBox, QSlider,
                             QListWidgetItem)
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore

from ftpretty import ftpretty
import sys
import os
from ftplib import FTP_TLS


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")
        self.setStyleSheet("background-color: #1C1C1C;color: white")

        widget = QListWidget()
        files = f.list('/', extra=True)

        # try:
        #     files = ftps.dir()
        # except ftpslib.error_perm as resp:
        #     if str(resp) == "550 No files found":
        #         print("No files in this directory")
        #     else:
        #         raise
        items = []
        # icon = QIcon(os.getcwd() + "/icons/directory.png")
        widget.setIconSize(QtCore.QSize(15, 15))
        for f in files:
            # items.append(QListWidgetItem(icon, f['name']))
            widget.addItem((QListWidgetItem(
                QIcon(os.getcwd() + '/icons/' +
                      ('directory' if f['directory'] == 'd' else 'file') +
                      '.png'), f['name'])))

        widget.currentItemChanged.connect(self.index_changed)
        widget.currentTextChanged.connect(self.text_changed)

        self.setCentralWidget(widget)

    def index_changed(self, i):  # Not an index, i is a QListItem
        print(i.text())

    def text_changed(self, s):  # s is a str
        print(s)


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()