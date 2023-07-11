import pandas as pd
import tkinter as tk
from tkinter import filedialog
import warnings
import lap_save_gui

warnings.simplefilter(action='ignore', category=pd.errors.SettingWithCopyWarning)
tk.Tk().withdraw()
file_path = filedialog.askopenfilename(filetypes=[(".csv", "*.csv")])
df = pd.read_csv(file_path, skiprows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 10])
specific_rows = [0, 1, 2, 3, 4, 5, 6, 7]
data_df = pd.read_csv(file_path, skiprows=lambda x: x not in specific_rows, usecols=[0, 1], header=None).T
new_header = data_df.iloc[0]
data_df = data_df[1:]
data_df.columns = new_header
simple_df = df[['Brake', 'LapDist', 'Speed', 'Lat', 'Lon', 'LapCurrentLapTime', 'Gear', 'Lap']]
simple_df.drop(simple_df.tail(5).index, inplace=True)
all_laps = sorted(list(simple_df['Lap'].value_counts().keys()))
valid_laps = all_laps.copy()
valid_laps.remove(valid_laps[0])
valid_laps.remove(valid_laps[::-1][0])
valid_lap_times = []
lap_dfs = []
for lap in valid_laps:
    lap_df = simple_df[simple_df['Lap'] == lap]
    if min(lap_df['Speed']) > 1:
        lap_time = max(lap_df['LapCurrentLapTime'])
        str_time = (str(int(lap_time / 60)) + ":" +
                    "{:02d}".format(int(lap_time % 60)) + str(lap_time % 60 - int(lap_time % 60))[1:6])
        valid_lap_times.append(str_time)
        lap_dfs.append(lap_df)
    else:
        valid_laps.remove(lap)


lap_save_gui.start(valid_laps, valid_lap_times, lap_dfs, data_df)
