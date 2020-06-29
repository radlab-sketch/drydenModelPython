
 If you find this code useful in your research, please consider citing using the following .bib entry:
 
 ```
@article{abichandani2020wind,
  title={Wind Measurement and Simulation Techniques in Multi-Rotor Small Unmanned Aerial Vehicles},
  author={Abichandani, Pramod and Lobo, Deepan and Ford, Gabriel and Bucci, Donald and Kam, Moshe},
  journal={IEEE Access},
  volume={8},
  pages={54910--54927},
  year={2020},
  publisher={IEEE}
}
 
 ```
 
 Text entry: 
 
 Abichandani, Pramod and Lobo, Deepan and Ford, Gabriel and Bucci, Donald and Kam, Moshe. "Wind Measurement and Simulation Techniques in Multi-Rotor Small Unmanned Aerial Vehicles." IEEE Access 8 (2020): 54910-54927.
 

## Implementation of Dryden wind turbulence model in python

The python file dryden_python_implementation.py contains the Python implemenation of the Dryden transfer functions. 

The python code implements the Dryden turbulence model defined by  transfer functions given in the US military in the handbook titled MIL-F-8785C. The ```dryden_wind_velocities(height, airspeed)```  function has two input parameter height and airspeed of the sUAV. The height and airspeed should be given in meters and meters/second respectively. The height and airspeed are the two parameters which are necessary to compute the wind turbulence velocities according to the Dryden transfer functions. The height defines the altitude in meters at which the UAV is operating. The airspeed refers to the speed of the sUAV relative to the surrounding air. The Dryden transfer functions have been defined in feet/second and thus a unit conversion was applied. 





The Dryden transfer function defined in MIL-F-8785C for the along-wind, cross-wind, and vertical-wind directions are as follows

**Along-wind:**

![along_wind_tf](/images/along_wind_tf.png)


**Cross-wind:**

![cross_wind_tf](/images/cross_wind_tf.png)

**Vertical-wind:**

![vertical_wind_tf](/images/vertical_wind_tf.png)



Each of the transfer functions depend on the following parameters, scale length L, turbulence intensity sigma, and airspeed V. The scale length and turbulence intensities for an altitude of less than 1000 feet have been defined as follows:

The scale lengths are given as

![scale_length](/images/scale_length_1.png)

where h is the altitude at which the UAV is operating.

The turbulence intensities are given as

![turbulence_intensity](/images/turbulence_intensity.png)

where W_20 is the wind speed in knots at 20 feet which has been predetermined and is used to define the turbulence level as light, moderate, and severe. 

```python
turbulence_level = 15
```

The turbulence level chosen is light for which the wind speed at 20 feet has been determined as 15 knots. 





```python
np.random.seed(23341)
samples1 = 10*np.random.normal(mean, std, size= num_samples)

np.random.seed(23342)
samples2 = 10*np.random.normal(mean, std, size= num_samples)

np.random.seed(23343)
samples3 = 10*np.random.normal(mean, std, size= num_samples)
```

The seeds used to generate the random number sequence have been obtained from MATLAB from the Dryden block in SIMULINK. The random number seed used in python is the same as used in MATLAB.


```python
  tf_u = u_transfer_function(height, airspeed)

  tf_v = v_transfer_function(height, airspeed)

  tf_w = w_transfer_function(height, airspeed)
```



Each of the transfer functions compute the transfer function using the 

```python
signal.TranferFunction(num_u, den_u)
```

which returns the coefficients of the computed transfer function. 



```python
  tout1, y1, x1 = signal.lsim(tf_u, samples1, t_p)
  y1_f = [i * 0.305 for i in y1]

  tout2, y2, x2 = signal.lsim(tf_v, samples2, t_p)
  y2_f = [i * 0.305 for i in y2]

  tout3, y3, x3 = signal.lsim(tf_w, samples3, t_p)
  y3_f = [i * 0.305 for i in y3]
```

The response to the transfer function is computed using the lsim() function which takes in the coefficients of the transfer function, the white gaussian noise, and the number of samples as input parameters. The result obtained is in feet/second so before plotting the data we apply a unit conversion by multiplying each element in the list with "0.305" to give the wind speed in meter/second. 

## Note on white gaussian noise: 

The following piece of code generates a sequence of 1000 equally spaced values from 0 - 5. The probability distribuiton of the sequence follows a gaussian distribution. 

```
    # Generate white gaussian noise 
    mean = 0
    std = 1 
    # create a sequence of 1000 equally spaced numeric values from 0 - 5
    t_p = np.linspace(0,5,1000)
    num_samples = 1000
```

According to the US military handbook the dryden transfer functions are applied on a band-limited white gaussian input to produce the desired Dryden turbulence spectrum. Alternatively we have provided a sample .csv file of the band-limited white gaussian noise inputs from MATLAB. To use the white noise inputs from MATLAB the following steps should be followed: 

**Step 1**
Uncomment the ```read_csv_file()``` function and define list variables ```t_w```, ```noise_1```, ```noise_2```, and ```noise_3``` 


**Step 2**
The response of the transfer function will change accordingly and will now be given as 

```python
  tout1, y1, x1 = signal.lsim(tf_u, n1, t_w)
  y1_f = [i * 0.305 for i in y1]

  tout2, y2, x2 = signal.lsim(tf_v, n2, t_w)
  y2_f = [i * 0.305 for i in y2]

  tout3, y3, x3 = signal.lsim(tf_w, n3, t_w)
  y3_f = [i * 0.305 for i in y3]
```

**Step 3** 
The methods use to plot the dryden specturm will now be given as 

```
plt.plot(t_w, y1_f, 'b')

plt.plot(t_w, y2_f, 'r')

plt.plot(t_w, y3_f, 'g')
```
