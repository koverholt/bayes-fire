#!/usr/bin/env python

"""
Read in the time and temperature data for the 
transient HRR example.
"""

import numpy as np

# Read in experimental data from file
data = np.genfromtxt('../Experimental_Data/time_temperature_data.csv',
                     delimiter=',', names=True)

# Set data variables
time = data['time']
temperature = data['temperature']
