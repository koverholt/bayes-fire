#!/usr/bin/env python

"""
Read in the heat flux data for the 
point source radiation example.
"""

import numpy as np

# Read in experimental data from file
data = np.genfromtxt('../Experimental_Data/heat_flux_data.csv',
                     delimiter=',', names=True)

# Set data variables
test = data['test']
distance = data['distance']
heat_flux = data['heat_flux']
