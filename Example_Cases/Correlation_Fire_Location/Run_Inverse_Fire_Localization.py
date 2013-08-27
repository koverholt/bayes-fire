#!/usr/bin/env python

import os, sys

os.chdir('Scripts')

print 'Running FDS 300 kW Inverse Fire Localization Model ...'
os.system('python heat_flux_localization_fds_300kW.py')

print 'Running FDS 1000 kW Inverse Fire Localization Model ...'
os.system('python heat_flux_localization_fds_1000kW.py')
