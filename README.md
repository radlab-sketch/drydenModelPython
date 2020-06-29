# drydenModelPython

The wind data here is generated using the Dryden Continuous Turbulence Model. Example of the data is stored in the csv file. 

Two python files here plot the individual components of wind (across-wind, crosswind, vertical) and the wind turbulence field. 


## Implementation of Dryden wind turbulence model in python

The following python code implements the Dryden turbulence model defined by  transfer functions given in the US military in the handbook titled MIL-F-8785C. 

The Dryden transfer function defined in MIL-F-8785C for the along-wind, cross-wind, and vertical-wind directions are as follows

**Along-wind:**

![along_wind_tf](/images/logo.png)

![image-20200405193227954](C:\Users\deepa\AppData\Roaming\Typora\typora-user-images\image-20200405193227954.png)

**Cross-wind:**

![cross_wind_tf](/images/logo.png)

**Vertical-wind:**

![vertical_wind_tf](/images/logo.png)



Each of the transfer functions depend on the following parameters, scale length L, turbulence intensity sigma, and airspeed V. The scale length and turbulence intensities for an altitude of less than 1000 feet have been defined as follows:

The scale lengths are given as

![scale_length](/images/logo.png)

where h is the altitude at which the UAV is operating.

The turbulence intensities are given as

![turbulence_intensity](/images/logo.png)

where W_20 is the wind speed in knots at 20 feet which has been predetermined and is used to define the turbulence level as light, moderate, and severe. 

```python
turbulence_level = 15
```

The turbulence level chosen is light for which the wind speed at 20 feet has been determined as 15 knots. 

### The dryden_wind_velocities() function:

The **dryden_wind_velocities(height, airspeed)** function has two input parameter height and airspeed of the sUAV. The height and airspeed should be given in meters and meters/second respectively. 

```python
np.random.seed(23341)
samples1 = 10*np.random.normal(mean, std, size= num_samples)

np.random.seed(23342)
samples2 = 10*np.random.normal(mean, std, size= num_samples)

np.random.seed(23343)
samples3 = 10*np.random.normal(mean, std, size= num_samples)
```

The seeds used to generate the random number sequence have been obtained from MATLAB from the Dryden block in SIMULINK. The random number seed used in python is the same as used in MATLAB.

The height and airspeed are the two parameters which are necessary to compute the wind turbulence velocities according to the Dryden transfer functions. The height defines the altitude in meters at which the UAV is operating and the wind velocities are needed. The airspeed defines the speed of the UAV relative to the surrounding air. The transfer functions have been defined in feet/second and thus we apply a unit conversion before sending it to the transfer function. 

```python
  tf_u = u_transfer_function(height, airspeed)

  tf_v = v_transfer_function(height, airspeed)

  tf_w = w_transfer_function(height, airspeed)
```



Each of the transfer functions compute the transfer function using the 

```python
signal.TranferFunction(num_u, den_u)
```

which returns the coefficients of the computed transfer function. Each of the transfer functions have been defined according to the definitions given at the start of this document. 



```python
  tout1, y1, x1 = signal.lsim(tf_u, samples1, t_p)
  y1_f = [i * 0.305 for i in y1]

  tout2, y2, x2 = signal.lsim(tf_v, samples2, t_p)
  y2_f = [i * 0.305 for i in y2]

  tout3, y3, x3 = signal.lsim(tf_w, samples3, t_p)
  y3_f = [i * 0.305 for i in y3]
```

The response to the transfer function is computed using the lsim() function which takes in the coefficients of the transfer function, the white gaussian noise, and the number of samples as input parameters. The result obtained is in feet/second so before plotting the data we apply a unit conversion by multiplying each element in the list with "0.305" to give the wind speed in meter/second. 



