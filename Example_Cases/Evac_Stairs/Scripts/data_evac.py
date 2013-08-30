#!/usr/bin/env python

"""
Read in the evac data.
"""

import numpy as np

# Read in experimental data from file
data = np.genfromtxt('../Experimental_Data/evac_data.csv',
                     delimiter=',', names=True)

# Set data variables
flow = data['flow'][:-5]
exit_distance = data['Exit_Distance'][:-5]
occupants = data['Occupants'][:-5]
effective_width = data['Effective_Width'][:-5]
