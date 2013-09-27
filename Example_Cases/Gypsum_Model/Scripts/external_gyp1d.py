#!/usr/bin/env python

"""Module for gyp1d functions"""

import numpy as np
import platform
import subprocess
import os

# Detect operating system
op_sys = platform.system()


def gen_input( matl ):
    """Generate gyp1d input file from template.

    Keyword arguments:
    matl = [ k1, k2, k3, k4, rho_0, c_p1, c_p2, c_p3, eps, Y1_0,
             A1, A2, E1, E2, dh1, dh2 ]
    """

    template = """
&matl 
    k_temps = 273.15, 448.15, 1088.15, 1473.15
    k_vals = %(k1)s, %(k2)s, %(k3)s, %(k4)s
    rho_0 = %(rho_0)s
    c_p = %(c_p1)s, %(c_p2)s, %(c_p3)s
    eps = %(eps)s 
    Y1_0 = %(Y1_0)s
    A = %(A1)s, %(A2)s
    E = %(E1)s, %(E2)s
    dh = %(dh1)s, %(dh2)s /

&scen
    L = 0.0159
    L_a = 0.092
    t_end = 3601
    H = 3.048 /

&numr
    N = 30
    N_t = 160000
    N_sol = 100 /
"""
    print template

    #  ==================================================
    #  = Generate gyp1d input file                      =
    #  ==================================================

#    outcase = template % {'abs_coeff':str(abs_coeff),
#                          'A':str(A),
#                          'E':str(E),
#                          'emissivity':str(emissivity),
#                          'HoR':str(HoR),
#                          'k':str(k),
#                          'rho':str(rho),
#                          'c':str(c)}
#
#    #  =====================
#    #  = Write FDS files =
#    #  =====================
#
#    casename = 'case'
#    filename = '../../../FDS_Model/' + casename + '.fds'
#
#    # Opens a new file, writes the FDS input file, and closes the file
#    f = open(filename, 'w')
#    f.write(outcase)
#    f.close()
#
#    return casename
#
#
#def run_fds(casename):
#    """Run FDS on case file."""
#    os.chdir('../../../FDS_Model')
#
#    # Run appropriate executable depending on operating system
#    if op_sys == 'Linux':
#        p = subprocess.Popen(['./fds_intel_linux_64', casename + '.fds'])
#        p.wait()
#    if op_sys == 'Darwin':
#        p = subprocess.Popen(['./fds_intel_osx_64', casename + '.fds'])
#        p.wait()
#    if op_sys == 'Windows':
#        p = subprocess.Popen(['./fds_intel_win_64', casename + '.fds'])
#        p.wait()
#
#    os.chdir('../Example_Cases/FDS_Mass_Loss_Rate/Scripts')
#
#
#def read_fds(casename):
#    """Read in FDS output."""
#    mlr_file = '../../../FDS_Model/' + casename + '_devc.csv'
#    mlrs = np.genfromtxt(mlr_file, delimiter=',', skip_header=2)
#
#    return mlrs
