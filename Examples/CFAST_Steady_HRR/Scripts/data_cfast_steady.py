#!/usr/bin/env python

"""
Read in the Steckler temperature data for the 
CFAST steady-state HRR example.
"""

import numpy as np

# Read in experimental data from file
data = np.genfromtxt('../Experimental_Data/hrr_temperature_data.csv',
                     delimiter=',', names=True)

# Set data variables
test = data['test']
door_width = data['door_width']
door_height = data['door_height']
hrr = data['hrr']
temperature = data['temperature']
tmp_a = data['tmp_a']
