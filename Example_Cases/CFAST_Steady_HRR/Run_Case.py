#!/usr/bin/env python

import os

os.chdir('Scripts/')

print 'Running CFAST_Steady_HRR ...'
os.system('python pymc_cfast_steady.py')
