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

# Assign dependent data variables
data_three_parameter['pre_evac_int'] = data_intensity['PreEvac_ave_intensity']
data_three_parameter['travel_int'] = data_intensity['TravelTime_ave_intensity']
data_three_parameter['exit_int'] = data_intensity['Exit_ave_intensity']
#added by PAR
data_three_parameter['exit_mu'] = data_intensity['Exit_mu']
data_three_parameter['preevac_mu'] = data_intensity['PreEvac_mu']
data_three_parameter['travel_mu'] = data_intensity['TravelTime_mu']
data_three_parameter['exit_alpha'] = data_intensity['Exit_alpha']
data_three_parameter['preevac_alpha'] = data_intensity['PreEvac_alpha']
data_three_parameter['travel_alpha'] = data_intensity['TravelTime_alpha']
# Assign independent data variables
data_three_parameter['occupants'] = data_intensity['Num_of_Occupants']
data_three_parameter['exit_distance'] = data_intensity['Exit_Distance']
data_three_parameter['type'] = data_intensity['Occupancy'] - 1
data_three_parameter['riser'] = data_intensity['Tread_Height']
data_three_parameter['tread'] = data_intensity['Tread_Depth']
data_three_parameter['evac_chair'] = data_intensity['Evacuation_Chair']
#added by PAR
data_three_parameter['eff_width'] = data_intensity['Effective_Width']
data_three_parameter['door_loc'] = data_intensity['NewDoor_Location']


data_ab = np.genfromtxt('../Experimental_Data/alphabeta.csv', delimiter=',',names=True)

data_alphabeta = {}

data_alphabeta['alpha'] = data_ab['alpha']
data_alphabeta['beta'] = data_ab['beta']

