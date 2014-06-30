#!/usr/bin/env python

import os
import sys

os.chdir('Scripts/')

matl = str(sys.argv[1])     # material ID
beta = str(sys.argv[2])     # heating rate, C/min
N_k = str(sys.argv[3])      # number of rxns

print 'Running TGA model ...'
os.system('python pymc_tga.py ' + matl + ' ' + beta + ' ' + N_k)
