#!/usr/bin/env python

import pylab as pl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def plot_ps_radiation_model(m):
    pl.plot(m.x.trace(), m.y.trace(), 'ko', ms=5, alpha=0.05)
    pl.axis([0, 10, 0., 10.])
    pl.xticks(fontsize=14)
    pl.xlabel('x Location (m)', fontsize=20)
    pl.yticks(fontsize=14)
    pl.ylabel('y Location (m)', fontsize=20)


def show_mcmc_steps(m):
    for i in range(len(m.x.trace())):
        pl.figure()
        pl.plot(m.x.trace()[:i], m.y.trace()[:i], 'k-', lw=2)
        pl.axis([0, 10, 0., 10.])
        pl.xticks(fontsize=14)
        pl.xlabel('x Location (m)', fontsize=20)
        pl.yticks(fontsize=14)
        pl.ylabel('y Location (m)', fontsize=20)
        pl.savefig('../Figures/MCMC_Steps/heat_flux_localization_' +
                   str(i) + '.pdf')

def plot_3d_hist(m):
    fig = pl.figure()
    ax = fig.add_subplot(111, projection='3d')
    hist, xedges, yedges = np.histogram2d(m.x.trace(), m.y.trace(), bins=20)

    elements = (len(xedges) - 1) * (len(yedges) - 1)
    xpos, ypos = np.meshgrid(xedges[:-1]-0.1, yedges[:-1]-0.1)

    xpos = xpos.flatten()
    ypos = ypos.flatten()
    zpos = np.zeros(elements)
    dx = 0.5 * np.ones_like(zpos)
    dy = dx.copy()
    dz = hist.flatten() + 0.001
    ax.set_xlabel('x Location (m)')
    ax.set_ylabel('y Location (m)')
    ax.set_zlabel('Frequency')

    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color='r', zsort='average')
