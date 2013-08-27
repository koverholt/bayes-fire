#!/usr/bin/env python

import os

os.chdir('Scripts/')

print 'Running FDS_Mass_Loss_Rate ...'
os.system('python pymc_fds.py')
