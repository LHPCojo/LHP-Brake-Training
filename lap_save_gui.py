import matplotlib as matplotlib
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtWidgets, QtGui
from PyQt5 import uic
import tkinter as tk
from tkinter import filedialog


matplotlib.use('Qt5Agg')


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
        fig.tight_layout()


class LHP_BASIS_LAP_IMPORTER(QtWidgets.QMainWindow):
    def __init__(self, valid_laps, valid_lap_times, lap_dfs, data_df):
        self.valid_laps = list(map(str, valid_laps))
        self.valid_lap_times = valid_lap_times
        self.lap_dfs = lap_dfs
        self.data_df = data_df
        QtWidgets.QMainWindow.__init__(self)
        self.ui = uic.loadUi('lap_save.ui', self)
        self.resize(888, 960)
        QtWidgets.QMainWindow.setWindowTitle(self, 'LHP Analytics Braking Tester')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("LHP_Logo.png"))
        self.setWindowIcon(icon)

        self.lapBox.addItems(self.valid_laps)
        self.lapBox.currentIndexChanged['QString'].connect(self.update_lap)
        self.lapBox.setCurrentIndex(0)

        self.time_label.setText(self.valid_lap_times[0])

        self.lineEdit_vehicle.setText(list(self.data_df['Vehicle'])[0])
        self.lineEdit_track.setText(list(self.data_df['Venue'])[0])

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.ui.gridLayout_4.addWidget(self.canvas, 2, 1, 1, 1)
        self.canvas.axes.plot(self.lap_dfs[0]['LapDist'], self.lap_dfs[0]['Brake'])

        min_threshold, max_threshold = self.lap_dfs[0]['Lon'].quantile([0.01, 0.99])

        lat_long_df = self.lap_dfs[0][(self.lap_dfs[0].Lon < max_threshold) & (self.lap_dfs[0].Lon > min_threshold)]

        self.canvas2 = MplCanvas(self, width=5, height=4, dpi=100)
        self.ui.gridLayout_4.addWidget(self.canvas2, 3, 1, 1, 1)
        self.canvas2.axes.scatter(lat_long_df['Lon'], lat_long_df['Lat'], c=lat_long_df['Brake'])

        self.pushButton.clicked.connect(self.save_selection)

    def update_lap(self, value):
        index = self.valid_laps.index(value)
        self.time_label.setText(self.valid_lap_times[index])
        self.canvas.axes.plot(self.lap_dfs[index]['LapDist'], self.lap_dfs[index]['Brake'])

        min_threshold, max_threshold = self.lap_dfs[index]['Lon'].quantile([0.01, 0.99])
        lat_long_df = self.lap_dfs[index][
            (self.lap_dfs[index].Lon < max_threshold) & (self.lap_dfs[index].Lon > min_threshold)]

        self.canvas2 = MplCanvas(self, width=5, height=4, dpi=100)
        self.ui.gridLayout_4.addWidget(self.canvas2, 3, 1, 1, 1)
        self.canvas2.axes.scatter(lat_long_df['Lon'], lat_long_df['Lat'], c=lat_long_df['Brake'])

    def save_selection(self):
        tk.Tk().withdraw()
        file_path = filedialog.asksaveasfilename(title="File Location to save baseline lap",
                                                 filetypes=[("csv file", ".csv")],
                                                 initialfile=self.lineEdit_track.text() + ".csv")
        index = self.valid_laps.index(self.lapBox.currentText())
        self.lap_dfs[index].drop(self.lap_dfs[index].tail(5).index, inplace=True)
        self.lap_dfs[index].to_csv(file_path, index=False)
        self.close()


def start(valid_laps, valid_lap_times, lap_dfs, data_df):
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = LHP_BASIS_LAP_IMPORTER(valid_laps, valid_lap_times, lap_dfs, data_df)
    mainWindow.show()
    sys.exit(app.exec_())
