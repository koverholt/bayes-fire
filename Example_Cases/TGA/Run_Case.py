#!/usr/bin/env python

import os

os.chdir('Scripts/')

print 'Running TGA model ...'
os.system('python pymc_tga.py')
