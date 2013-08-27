#!/usr/bin/env python

import os

os.chdir('Scripts/')

print 'Running Correlation_Fire_Location (300 kW) ...'
os.system('python heat_flux_localization_fds_300kW.py')

print 'Running Correlation_Fire_Location (1000 kW) ...'
os.system('python heat_flux_localization_fds_1000kW.py')
