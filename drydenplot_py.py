
import scipy.io as sio
import numpy as np
from matplotlib import pyplot as plt
import csv
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from mpl_toolkits.mplot3d import axes3d



u = []
v = []
w = []
t = []
timeval = 0
def read_csv_file():
    global timeval
    with open('wind_data.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
                t.append(float(row[0]))
                u.append(float(row[1]))
                v.append(float(row[2]))
                w.append(float(row[3]))
                

def main():
    read_csv_file()
    ax1 = plt.subplot(311)
    plt.plot(t,u, 'b')
    plt.ylabel('along-wind in m/s')
    plt.subplot(312)
    plt.plot(t,v, 'r')
    plt.ylabel('cross-wind')
    plt.subplot(313)
    plt.plot(t,w, 'g')
    plt.ylabel('vertical-wind')
    plt.xlabel('time of flight in sec')
    fig2 = plt.figure(2)
    ax2 = fig2.gca(projection='3d')
    along, cross, vert = np.meshgrid(u[70:80],v[40:50],w[40:50])
    x = np.sin(np.pi * along) * np.cos(np.pi * cross) * np.cos(np.pi * vert)
    y = -np.cos(np.pi * along) * np.sin(np.pi * cross) * np.cos(np.pi * vert)
    z = (np.sqrt(2.0 / 3.0) * np.cos(np.pi * along) * np.cos(np.pi * cross) * np.sin(np.pi * vert))
   
    c = np.arctan2(y, x)
    c = (c.ravel() -c.min()) / c.ptp()
    c = np.concatenate((c, np.repeat(c,2)))
    c = plt.cm.hsv(c)

    ax2.quiver(along, cross, vert, x, y, z, length = 0.008, colors=c, normalize=True)
    
    ax2.set_xlabel('along wind (m/sec)')
    ax2.set_ylabel('cross wind (m/sec)')
    ax2.set_zlabel('vertical wind (m/sec)')
    
    plt.show()
main()

