
# If you find this work useful please consider citing using the following .bib or text entry:

#Text entry
#Abichandani, Pramod and Lobo, Deepan and Ford, Gabriel and Bucci, Donald and Kam, Moshe. "Wind Measurement and Simulation Techniques in Multi-Rotor Small Unmanned Aerial Vehicles." IEEE Access 8 (2020): 54910-54927.

# Bib entry

# @article{abichandani2020wind,
#   title={Wind Measurement and Simulation Techniques in Multi-Rotor Small Unmanned Aerial Vehicles},
#   author={Abichandani, Pramod and Lobo, Deepan and Ford, Gabriel and Bucci, Donald and Kam, Moshe},
#   journal={IEEE Access},
#   volume={8},
#   pages={54910--54927},
#   year={2020},
#   publisher={IEEE}
# }

###########################################################################################################
import scipy.io as sio
import numpy as np
import math
from scipy.signal import butter, lfilter, freqz, firwin
from scipy import signal
from matplotlib import pyplot as plt
import csv
from matplotlib.colors import Normalize

#Low altitude Model
#transfer function for along-wind
def u_transfer_function(height, airspeed):
    #turbulence level defines value of wind speed in knots at 20 feet
    # turbulence_level = 15 * 0.514444 # convert speed from knots to meters per second
    turbulence_level = 15 
    length_u = height / ((0.177 + 0.000823*height)**(0.2))
    # length_u = 1750
    sigma_w = 0.1 * turbulence_level 
    sigma_u = sigma_w / ((0.177 + 0.000823*height) ** (0.4))
    num_u = [sigma_u * (math.sqrt((2 * length_u) / (math.pi * airspeed))) * airspeed]
    den_u = [length_u, airspeed]
    H_u = signal.TransferFunction(num_u, den_u)
    return H_u

#transfer function for cross-wind
def v_transfer_function(height, airspeed):
    #turbulence level defines value of wind speed in knots at 20 feet
    # turbulence_level = 15 * 0.514444 # convert speed from knots to meters per second
    turbulence_level = 15 
    length_v = height / ((0.177 + 0.000823*height)**(0.2))
    # length_v = 1750
    sigma_w = 0.1 * turbulence_level 
    sigma_v = sigma_w / ((0.177 + 0.000823*height) ** (0.4))
    b = sigma_v * (math.sqrt((length_v) / (math.pi * airspeed)))
    Lv_V = length_v / airspeed
    num_v = [(math.sqrt(3)*Lv_V*b), b]
    den_v = [(Lv_V**2), 2*Lv_V, 1]
    H_v = signal.TransferFunction(num_v, den_v)
    return H_v

#transfer function for vertical-wind
def w_transfer_function(height, airspeed):
    #turbulence level defines value of wind speed in knots at 20 feet
    # turbulence_level = 15 * 0.514444 # convert speed from knots to meters per second
    turbulence_level = 15 
    length_w = height
    # length_w = 1750
    sigma_w = 0.1 * turbulence_level 
    c = sigma_w * (math.sqrt((length_w) / (math.pi * airspeed)))
    Lw_V = length_w / airspeed
    num_w = [(math.sqrt(3)*Lw_V*c), c]
    den_w = [(Lw_V**2), 2*Lw_V, 1]
    H_v = signal.TransferFunction(num_w, den_w)
    return H_v

# t_w = []
# noise1 = []
# noise2 = []
# noise3 = []
# def read_csv_file():
#     with open('white_noise.csv') as csv_file:
#         csv_reader = csv.reader(csv_file, delimiter=',')
#         for row in csv_reader:
#                 t_w.append(float(row[0]))
#                 noise1.append(float(row[1]))
#                 noise2.append(float(row[2]))
#                 noise3.append(float(row[3]))




def dryden_wind_velocities(height, airspeed):
    # height and airspeed coverted to feet and feet/sec
    height = float(height) * 3.28084
    airspeed = float(airspeed) * 3.28084
    # Generate white gaussian noise 
    mean = 0
    std = 1 
    # create a sequence of 1000 equally spaced numeric values from 0 - 5
    t_p = np.linspace(0,5,1000)
    num_samples = 1000
    
    # the random number seed used same as from SIMULINK blockset
    np.random.seed(23341)
    samples1 = 10*np.random.normal(mean, std, size= num_samples)

    np.random.seed(23342)
    samples2 = 10*np.random.normal(mean, std, size= num_samples)

    np.random.seed(23343)
    samples3 = 10*np.random.normal(mean, std, size= num_samples)

    #generate tranfer function for dryden wind speeds in along wind direction, cross-wind, and vertical-wind directions
    tf_u = u_transfer_function(height, airspeed)
    tf_v = v_transfer_function(height, airspeed)
    tf_w = w_transfer_function(height, airspeed)

    # Scale factor used to scale the white gaussian noise inputs. The scale factor used here is 10
    #scale_factor = 10

    # n1 = [i * scale_factor for i in noise1]
    # n2 = [i * scale_factor for i in noise2]
    # n3 = [i * scale_factor for i in noise3]

    # compute response to tranfer function
    tout1, y1, x1 = signal.lsim(tf_u, samples1, t_p)
    # tout1, y1, x1 = signal.lsim(tf_u, n1, t_w)
    # covert obtained values to meters/second
    y1_f = [i * 0.305 for i in y1]
    tout2, y2, x2 = signal.lsim(tf_v, samples2, t_p)
    # tout2, y2, x2 = signal.lsim(tf_v, n2, t_w)
    y2_f = [i * 0.305 for i in y2]
    tout3, y3, x3 = signal.lsim(tf_w, samples3, t_p)
    # tout3, y3, x3 = signal.lsim(tf_w, n3, t_w)
    y3_f = [i * 0.305 for i in y3]

    #plots for along-wind velocities generated using Python
    plt.figure(1)

    plt.plot(t_p, y1_f, 'b')
    # plt.plot(t_w, y1_f, 'b')
    plt.ylabel('along-wind in m/s (P)')
    plt.xlabel('time in seconds')
    plt.grid(True)

    #plots for cross-wind velocities generated using Python
    plt.figure(2)

    plt.plot(t_p, y2_f, 'r')
    # plt.plot(t_w, y2_f, 'r')
    plt.ylabel('cross-wind in m/s (P)')
    plt.xlabel('time in seconds')
    plt.grid(True)

    #plots for vertical-wind velocities generated using Python
    plt.figure(3)

    plt.plot(t_p, y3_f, 'g')
    # plt.plot(t_w, y3_f, 'g')
    plt.ylabel('vertical-wind in m/s (P)')
    plt.xlabel('time in seconds')
    plt.grid(True)

    # Show all plots
    plt.show()




              

def main():
    h = input("please enter altitude in meters")
    a = input("please enter airspeed in meters/second")
    dryden_wind_velocities(h, a)


main()

