#!/usr/bin/env python

"""
Read in normalized experimental data: [ T (K), w ]
"""

import numpy as np

beta = 5./60.       # heating rate, K/s

# Read in experimental data from file
data = np.genfromtxt('../Experimental_Data/gypsum_5Kmin.csv', delimiter=',', skiprows=1)

T = data[:,0]       # temperature, K
w = data[:,1]       # normalized total mass
