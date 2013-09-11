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

# Read in experimental data from file
data_intensity = np.genfromtxt('../Experimental_Data/mu_alpha_beta_intensity.csv',
                                     delimiter=',', names=True)

data_three_parameter = {}

# Assign independent data variables
data_three_parameter['pre_evac_int'] = data_intensity['PreEvac_ave_intensity']
data_three_parameter['travel_int'] = data_intensity['TravelTime_ave_intensity']
data_three_parameter['exit_int'] = data_intensity['Exit_ave_intensity']

# Assign dependent data variables
data_three_parameter['occupants'] = data_intensity['Num_of_Occupants']
data_three_parameter['exit_distance'] = data_intensity['Exit_Distance']
data_three_parameter['type'] = data_intensity['Occupancy'] - 1
data_three_parameter['riser'] = data_intensity['Tread_Height']
data_three_parameter['tread'] = data_intensity['Tread_Depth']
data_three_parameter['evac_chair'] = data_intensity['Evacuation_Chair']
