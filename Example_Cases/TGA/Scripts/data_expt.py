#!/usr/bin/env python

"""
Read in normalized experimental data: [ T (K), w ]
"""

import numpy as np

## Read in experimental data from file
#data = np.genfromtxt('../Experimental_Data/mehaffey_1994.csv',
#                     delimiter=',', names=True)
#
## Set data variables
#T = data['T']       # temperature, K
#w = data['w']       # normalized mass

data = np.genfromtxt('../Experimental_Data/tga_usg_ulx_5Kmin.csv', delimiter=',', skiprows=1)

T = data[:,0]       # temperature, K
w = data[:,1]       # normalized total mass
