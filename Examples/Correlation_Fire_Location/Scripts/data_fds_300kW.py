#!/usr/bin/env python

"""
Read in the heat flux data from FDS for
the 300 kW fire localization example.
"""

import numpy as np

# Read in experimental data from file
fds_data = np.genfromtxt('../FDS_Output_Files/burn_300kW_devc.csv',
                         skip_header=1, delimiter=',', names=True)

x_gauge = np.array([1])
y_gauge = np.array([0])
heat_flux = np.array([])

heat_flux = np.append(heat_flux, fds_data[-1]['HF_A1_GAUGE'])
# heat_flux = np.append(heat_flux, fds_data[-1]['HF_A2_GAUGE'])
# heat_flux = np.append(heat_flux, fds_data[-1]['HF_A3_GAUGE'])
# heat_flux = np.append(heat_flux, fds_data[-1]['HF_A4_GAUGE'])
# heat_flux = np.append(heat_flux, fds_data[-1]['HF_A5_GAUGE'])
# heat_flux = np.append(heat_flux, fds_data[-1]['HF_A6_GAUGE'])
