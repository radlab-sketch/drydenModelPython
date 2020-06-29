## Implementation of Dryden wind turbulence model in python

The following python code implements the Dryden turbulence model defined by  transfer functions given in the US military in the handbook titled MIL-F-8785C. 

The Dryden transfer function defined in MIL-F-8785C for the along-wind, cross-wind, and vertical-wind directions are as follows

**Along-wind:**

![image-20200405193227954](C:\Users\deepa\AppData\Roaming\Typora\typora-user-images\image-20200405193227954.png)

**Cross-wind:**

![image-20200405193255202](C:\Users\deepa\AppData\Roaming\Typora\typora-user-images\image-20200405193255202.png)

**Vertical-wind:**

![image-20200405193327040](C:\Users\deepa\AppData\Roaming\Typora\typora-user-images\image-20200405193327040.png)



Each of the transfer functions depend on the following parameters, scale length L, turbulence intensity sigma, and airspeed V. The airspeed is obtained as input from the user. The scale length and turbulence intensities for an altitude of less than 1000 feet have been defined as follows:

The scale lengths are given as

![image-20200405193856644](C:\Users\deepa\AppData\Roaming\Typora\typora-user-images\image-20200405193856644.png)

where h is the altitude at which the UAV is operating in and is obtained as input from the user as 'height'. 

The turbulence intensities are given as

![image-20200405193912605](C:\Users\deepa\AppData\Roaming\Typora\typora-user-images\image-20200405193912605.png)

where W_20 is the wind speed in knots at 20 feet which has been predetermined and is used to define the turbulence level as light, moderate, and severe. 

```python
turbulence_level = 15
```

The turbulence level chosen is light for which the wind speed at 20 feet has been determined as 15 knots. The height 'h' is obtained from the user as input.



### The main() function:

  read_csv_file_1(): creates three lists for the wind velocities generated using SIMULINK block in MATLAB by reading the CSV file wind_data_test 

  read_csv_file_2(): creates a list for the number of samples generated in SIMULINK using MATLAB by reading the CSV file tout.csv 

  read_csv_file_3(): creates three lists for the band limited white gaussian noise samples generated using SIMULINK in MATLAB by reading the CSV file white_noise

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
  height = input("please enter height in meters")
  height = float(height) * 3.28084
  airspeed = input("please enter airspeed in meters/second")
  airspeed = float(airspeed) * 3.28084
```



The height and airspeed are the two parameters which are necessary to compute the wind turbulence velocities according to the Dryden transfer functions. The application takes in these two inputs from the user. The height defines the altitude in meters at which the UAV is operating and the wind velocities are needed. The airspeed defines the speed of the UAV relative to the surrounding air. The transfer functions have been defined in feet/second and thus we apply a unit conversion before sending it to the transfer function. 

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

The response to the transfer function is computed using the lsim() function which takes in the coefficients of the transfer function, the white gaussian noise, and the number of samples as input parameters. The result obtained is in feet/second so before plotting the data we apply a unit conversion by multiplying each element in the list with "3.05" to give the wind speed in meter/second. 