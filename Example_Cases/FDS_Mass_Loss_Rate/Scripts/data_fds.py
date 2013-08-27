#!/usr/bin/env python

"""
Read in the heat flux data for the 
FDS mass loss rate example.
"""

import numpy as np

# Read in experimental data from file
data = np.genfromtxt('../Experimental_Data/mlr_cone_data.csv',
                     delimiter=',', names=True)

# Set data variables
time = data['time']
mlr = data['mlr']
