from matplotlib import pyplot as plt
from windrose import WindroseAxes
import matplotlib.cm as cm
import numpy as np

import csv


windspeed = []
winddirection = []
def read_csv_file():
    with open('speeddata.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
                windspeed.append(float(row[0]))
                winddirection.append(float(row[1]))



def main():
    read_csv_file()
    ax = WindroseAxes.from_ax()
    plt.title('Wind speed in meters/second and Direction in degrees')
    ax.bar(winddirection, windspeed, normed=True, opening=0.8, edgecolor='white')
    ax.set_legend()
    plt.show()
main()
