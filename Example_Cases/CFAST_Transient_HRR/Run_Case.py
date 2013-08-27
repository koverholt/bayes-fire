#!/usr/bin/env python

import os

os.chdir('Scripts/')

print 'Running CFAST_Transient_HRR ...'
os.system('python pymc_cfast_transient.py')
