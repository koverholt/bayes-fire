#!/usr/bin/env python

"""Module for FDS functions"""

import numpy as np
import platform
import subprocess
import os

# Detect operating system
op_sys = platform.system()


def gen_input(abs_coeff, A, E, emissivity, HoR, k, rho, c):
    """Generate FDS input file from template.

    Keyword arguments:
    abs_coeff -- Absorption coefficient of solid material
    A -- Pre exponential of solid material
    E -- Activation energy of solid material
    emissivity -- Emissivity of solid material
    HoR -- Heat of reaction of solid material
    k -- Thermal conductivity of solid material
    rho -- Density of solid material
    c -- Specific heat of solid material
    """

    template = """&HEAD CHID='case', TITLE='Black PMMA at 50 kW/m2, No Gas Phase Reaction' /

&MESH IJK=3,3,4, XB=-0.15,0.15,-0.15,0.15,0.0,0.4 /  Mesh is just to make FDS run

&TIME T_END=515., WALL_INCREMENT=1, DT=0.1 /  Force FDS to do solid phase calc every time step
&MISC  Y_O2_INFTY=0.01 /

&REAC FUEL='METHANE'/  No gas phase reaction with 1%% O2 concentration

&MATL ID='BLACKPMMA'
      ABSORPTION_COEFFICIENT=%(abs_coeff)s
      N_REACTIONS=1
      A(1) = %(A)s
      E(1) = %(E)s
      EMISSIVITY=%(emissivity)s
      SPEC_ID='METHANE'
      NU_SPEC=1.
      HEAT_OF_REACTION=%(HoR)s
      HEAT_OF_COMBUSTION=25200.
      CONDUCTIVITY=%(k)s
      DENSITY=%(rho)s
      SPECIFIC_HEAT=%(c)s /

&MATL ID='FOAMGLAS'
      CONDUCTIVITY = 0.08
      SPECIFIC_HEAT = 0.84
      DENSITY = 120. /

&SURF ID='PMMA SLAB'
      COLOR='BLACK'
      MATL_ID='BLACKPMMA','FOAMGLAS'
      THICKNESS=0.0085,0.01
      HEAT_TRANSFER_COEFFICIENT=0.
      EXTERNAL_FLUX=52 /  External Flux is ONLY for this simple demo exercise

&VENT XB=-0.05,0.05,-0.05,0.05,0.0,0.0, SURF_ID = 'PMMA SLAB' /

&VENT MB='XMIN', SURF_ID='OPEN' /
&VENT MB='XMAX', SURF_ID='OPEN' /
&VENT MB='YMIN', SURF_ID='OPEN' /
&VENT MB='YMAX', SURF_ID='OPEN' /
&VENT MB='ZMAX', SURF_ID='OPEN' /

&DUMP DT_DEVC=5. /

&DEVC XYZ=0.0,0.0,0.0, IOR=3, QUANTITY='WALL TEMPERATURE',     ID='temp' /
&DEVC XYZ=0.0,0.0,0.0, IOR=3, QUANTITY='BURNING RATE',         ID='MLR' /
&DEVC XYZ=0.0,0.0,0.0, IOR=3, QUANTITY='WALL THICKNESS',       ID='thick' /

&TAIL /"""

    #  ==================================================
    #  = Generate FDS input file and fire object file =
    #  ==================================================

    outcase = template % {'abs_coeff':str(abs_coeff),
                          'A':str(A),
                          'E':str(E),
                          'emissivity':str(emissivity),
                          'HoR':str(HoR),
                          'k':str(k),
                          'rho':str(rho),
                          'c':str(c)}

    #  =====================
    #  = Write FDS files =
    #  =====================

    casename = 'case'
    filename = '../../../FDS_Model/' + casename + '.fds'

    # Opens a new file, writes the FDS input file, and closes the file
    f = open(filename, 'w')
    f.write(outcase)
    f.close()

    return casename


def run_fds(casename):
    """Run FDS on case file."""
    os.chdir('../../../FDS_Model')

    # Run appropriate executable depending on operating system
    if op_sys == 'Linux':
        p = subprocess.Popen(['./fds_intel_linux_64', casename + '.fds'])
        p.wait()
    if op_sys == 'Darwin':
        p = subprocess.Popen(['./fds_intel_osx_64', casename + '.fds'])
        p.wait()
    if op_sys == 'Windows':
        p = subprocess.Popen(['./fds_intel_win_64', casename + '.fds'])
        p.wait()

    os.chdir('../Example_Cases/FDS_Mass_Loss_Rate/Scripts')


def read_fds(casename):
    """Read in FDS output."""
    mlr_file = '../../../FDS_Model/' + casename + '_devc.csv'
    mlrs = np.genfromtxt(mlr_file, delimiter=',', skip_header=2)

    return mlrs
