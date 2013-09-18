#!/usr/bin/env python

import os

os.chdir('Scripts/')

print 'Processing Evacuation Data, Flow vs. Exit Distance ...'
os.system('python run_evac_flow_exit_dist.py')

print 'Processing Evacuation Data, Flow vs. Occupants ...'
os.system('python run_evac_flow_occupants.py')

print 'Processing Evacuation Data, Flow vs. Effective Width ...'
os.system('python run_evac_flow_effective_width.py')

print 'Processing Evacuation Data, Higher Order Models ...'
os.system('python run_evac_flow_higher_order.py')

print 'Processing Evacuation Data, Three Parameter Models ...'
os.system('python run_evac_flow_three_parameter.py')
