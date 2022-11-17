import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QToolBar, QMenu, QGridLayout, QMenuBar, QPlainTextEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore, QtWidgets
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

matplotlib.use('Qt5Agg')


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 tabs - pythonspot.com'
        self.setWindowTitle(self.title)
        # left top width height
        self.setGeometry(0, 0, 300, 200)

        self.table_widget = MyTableWidget(self)
        # self.toolbar = QToolBar("My main toolbar")
        # self.addToolBar(self.toolbar)
        self.setCentralWidget(self.table_widget)
        # layout = QGridLayout()
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        self.actions = {0: ['New Profile', self], 1: ['Load Profile...', self]}
        for k, v in self.actions.items():
            file_menu.addAction(QAction(*v))

        # imp_menu = QMenu('Import', self)
        # imp_act = QAction('Import mail', self)
        # imp_menu.addAction(imp_act)
        # file_menu.addMenu(imp_menu)

        # self.show()
    def on_import_click(self, s):
        print("click", s)


class MyTableWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tabs.resize(300, 200)

        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab_names = [
            'Bar',
        ]
        # Add tabs
        self.tabs.addTab(self.tab1, "Tab 1")
        self.tabs.addTab(self.tab2, "Tab 2")

        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        self.sc.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])

        # Create first tab
        self.tab1.layout = QVBoxLayout(self)
        self.pushButton1 = QPushButton("PyQt5 button")
        # self.pushButton1 = QPushButton("PyQt5 button")
        self.tab1.layout.addWidget(self.sc)
        self.tab1.setLayout(self.tab1.layout)

        # self.setCentralWidget(sc)

        self.tab2.layout = QVBoxLayout(self)
        self.tab2.setLayout(self.tab2.layout)
        self.tab2.layout.addWidget(self.pushButton1)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        # self.show()

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(),
                  currentQTableWidgetItem.column(),
                  currentQTableWidgetItem.text())


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = App()
#     sys.exit(app.exec_())
app = QApplication(sys.argv)
screen = App()
screen.show()
sys.exit(app.exec_())