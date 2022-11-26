import sys
import random
from tkinter import filedialog as fd
import pandas as pd
import pathlib
import datetime
# import models
from models import session, Spreadsheet, init_db
from sqlalchemy import select
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QShortcut
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import pyqtSlot
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

matplotlib.use('Qt5Agg')


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=10, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        # self.axes.xlim([0, 30])
        # self.axes.set_xlim([0, 30])
        super(MplCanvas, self).__init__(self.fig)

    def redraw(self):
        # self.axes = plot
        self.fig.clf()


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        init_db()
        # con = sqlite3.connect("tutorial.db")
        # self.cur = con.cursor()
        # self.db = orm_sqlite.Database('example.db')
        # Spreadsheet.objects.backend = self.db
        self.title = 'PyQt5 tabs - pythonspot.com'
        self.setWindowTitle(self.title)
        # left top width height
        self.setGeometry(0, 0, 1500, 800)
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        menubar = self.menuBar()
        self.menu_items = {
            'File': {
                0: [['Import', self], self.import_spreadsheet, 'Ctrl+O'],
                1: [['Load Profile...', self], self.import_spreadsheet,
                    'Ctrl+l']
            },
            'Something': {
                0: [['something_New Profile', self], self.import_spreadsheet,
                    'Ctrl+Y'],
                1: [['something_Load Profile...', self],
                    self.import_spreadsheet, 'Ctrl+W'],
                'Foobar': {
                    0: [['foobar_New Profile', self], self.import_spreadsheet,
                        'Ctrl+Q'],
                    'more_foobar': {
                        0: [['foobar_Load Profile...', self],
                            self.import_spreadsheet],
                        1: [['even more foobar_Profile...', self],
                            self.import_spreadsheet]
                    },
                    1: [['foobar_Load Profile...', self],
                        self.import_spreadsheet],
                }
            }
        }
        self.hotkeys = []
        for k, branch in self.menu_items.items():
            self.add_branch(menubar, branch, k)

    def add_branch(self, menubar, branch, k):
        if type(branch) is dict:
            file_menu = menubar.addMenu(k)
            for key, action in branch.items():
                self.add_branch(file_menu, action, key)
        else:
            action = QAction(*branch[0])
            action.triggered.connect(branch[1]) if callable(branch[1]) else ''
            self.define_hotkey(branch) if len(branch) == 3 else ''
            menubar.addAction(action)

    def define_hotkey(self, branch):
        key_combination = branch[2]
        self.hotkeys.append(QShortcut(QKeySequence(key_combination), self))
        self.hotkeys[-1].activated.connect(branch[1])

    def import_spreadsheet(self):
        filenames = fd.askopenfilenames(title="Import Spreadsheet(s)",
                                        initialdir='./spreadsheet_dir',
                                        filetypes=(("", "*.csv"), ("", ".xls"),
                                                   ("", ".xlsx")))
        for name in filenames:
            file_ext = pathlib.Path(name).suffix
            appropriate_methods = {
                ".csv": pd.read_csv,
                ".xls": pd.read_excel,
                ".xlsx": pd.read_excel
            }

            # n_data = 50
            # self.xdata = list(range(n_data))
            # self.ydata = [random.randint(0, 10) for i in range(n_data)]
            # self.update_plot()
            result = appropriate_methods[file_ext](name)

            for row in result.values.tolist():
                print(row)
                spreadsheet = Spreadsheet(
                    row[2], datetime.datetime.strptime(row[0], '%Y-%m-%d'),
                    row[4])
                spreadsheet.save()
            # for header in result.head().columns:
            # print(result)

    def update_plot(self):
        # Drop off the first y element, append a new one.
        self.ydata = self.ydata[1:] + [random.randint(0, 10)]
        self.table_widget.sc.axes.cla()  # Clear the canvas.
        self.table_widget.sc.axes.plot(self.xdata, self.ydata, 'r')
        # Trigger the canvas to update and redraw.
        self.table_widget.sc.draw()


# class Spreadsheet(orm_sqlite.Model):
#     id = orm_sqlite.IntegerField(primary_key=True)
#     name = orm_sqlite.StringField()
#     amount = orm_sqlite.FloatField()
#     date = orm_sqlite.StringField()


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

        self.sc = MplCanvas(self, width=15, height=4, dpi=100)
        # stmt = select(models.Spreadsheet).where(models.Spreadsheet.amount < 0)
        # print(models.session.execute(stmt))
        # print(models.session.query( models.Spreadsheet).filter(models.Spreadsheet.amount < 0))
        # print(models.Spreadsheet.credits)

        # result = models.Spreadsheet.credits(models.Spreadsheet)
        # for r in result:
        #     print(r.name)

        # spreadsheet = (session.query(models.Spreadsheet).filter_by(
        #     name='ELECTRONIC WITHDRAWAL ATT')).first()

        # spreadsheets = session.query(Spreadsheet).filter(
        #     Spreadsheet.amount < 0)
        x_axis = []
        y_axis = []
        spreadsheets = Spreadsheet.credits(Spreadsheet)
        for spreadsheet in spreadsheets:
            # print(spreadsheet.amount)
            x_axis.append(spreadsheet.date)
            y_axis.append(spreadsheet.amount * -1)

        for x in x_axis:
            print(x)
        # Spreadsheet.name
        self.sc.axes.plot(x_axis, y_axis)
        # self.sc.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])

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
