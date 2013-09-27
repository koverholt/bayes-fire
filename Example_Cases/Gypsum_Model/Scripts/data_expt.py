#!/usr/bin/env python

"""
Read in the temperature data for the 
gysum board partition ASTM E119 experiment.
"""

import numpy as np

# Read in experimental data from file
data = np.genfromtxt('../Experimental_Data/takeda_1998.csv',
                     delimiter=',', names=True)

# Set data variables
time = data['time']     # times, seconds
T_1b = data['T_1b']     # temperatures at back of exposed board, K
T_2b = data['T_2b']     # temperatures at back of unexposed board, K
