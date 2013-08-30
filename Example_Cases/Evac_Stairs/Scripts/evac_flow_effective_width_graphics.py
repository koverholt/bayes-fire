#!/usr/bin/env python

"""Module for setting up plotting routines"""

import pylab as pl
import data_evac


def plot_all_data():
    """Plot the data and decorate the output."""
    plot_evac_data()
    decorate_plot()


def plot_evac_data():
    """Plot the measured data."""
    pl.plot(data_evac.effective_width,
            data_evac.flow,
            'bs', ms=10, mew=0, label='Exp. Data')


def plot_linear_model(m):
    """
    Plot each realization from the linear model.
    """
    effective_width = pl.arange(0., 1.3, 0.001)
    for theta_t in m.theta.trace():
        flow = theta_t[0]*effective_width + theta_t[1]
        pl.plot(effective_width, flow,
                color='gray', alpha=.75, zorder=-1)

    theta = m.theta.stats()['mean']
    flow = theta[0]*effective_width + theta[1]
    pl.plot(effective_width, flow,
            color='purple', linewidth=5,
            label='Linear Model')
    decorate_plot()


def plot_power_law_model(m,
                            color='green',
                            label='Power Law Model'):
    """
    Plot each realization from the power law.
    """
    effective_width = pl.arange(0.01, 1.3, 0.001)
    flow_trace = []
    for theta in m.theta.trace():
        flow = theta[0] * effective_width**theta[1]
        pl.plot(effective_width, flow,
                color='gray', alpha=.75, zorder=-1)
        flow_trace.append(flow)

    pl.plot(effective_width, pl.mean(flow_trace, axis=0),
            color=color, linewidth=5,
            label=label)
    decorate_plot()


def decorate_plot():
    """Decorate the plot with labels."""
    pl.axis([0.6, 1.3, 0.1, 0.9])
    pl.legend(numpoints=1, prop=dict(size=20), fancybox=True)
    pl.xticks(fontsize=20)
    pl.xlabel('Effective Width (m)', fontsize=24)
    pl.yticks(fontsize=20)
    pl.ylabel('Flow (people/s)', fontsize=24)


# def plot_joint_density(X, Y, bounds=None):
#     """
#     Plot joint density of X and Y.

#     Used in example 4 to explore model convergence.
#     """
#     if bounds:
#         X_min, X_max, Y_min, Y_max = bounds
#     else:
#         X_min = X.min()
#         X_max = X.max()
#         Y_min = Y.min()
#         Y_max = Y.max()

#     pl.plot(X, Y,
#             linestyle='none', marker='o',
#             color='green', mec='green',
#             alpha=.75, zorder=-99)

#     import scipy.stats
#     gkde = scipy.stats.gaussian_kde([X, Y])
#     x, y = pl.mgrid[X_min:X_max:(X_max-X_min)/25.,
#                     Y_min:Y_max:(Y_max-Y_min)/25.]
#     z = pl.array(gkde.evaluate([x.flatten(), y.flatten()])).reshape(x.shape)
#     pl.contour(x, y, z, linewidths=2)

#     pl.axis([X_min, X_max, Y_min, Y_max])


def plot_predicted_data(y_pred):
    """
    Plot predicted data side-by-side in subplots.

    Used in example 5 to explore model convergence.
    """
    pl.subplot(3,1,1)
    plot_evac_data()
    decorate_plot()
    pl.xlabel('')
    pl.ylabel('')

    pl.subplot(3,1,2)
    plot_predicted_sample(data_evac.effective_width, y_pred)
    decorate_plot()
    pl.xlabel('')

    pl.subplot(3,1,3)
    plot_predicted_sample(data_evac.effective_width, y_pred)
    decorate_plot()
    pl.ylabel('')

    pl.subplots_adjust(hspace=0.)


def plot_predicted_sample(x, y_pred):
    """Used by the plot_predicted_data function."""
    t = pl.rand() * len(y_pred.trace())
    y_t = y_pred.trace()[t]
    pl.plot(x, y_t, 'g^', ms=12, mew=0, label='Prediction')
