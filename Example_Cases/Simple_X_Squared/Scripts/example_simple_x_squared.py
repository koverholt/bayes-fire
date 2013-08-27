#!/usr/bin/env python

"""
Simplest PyMC simulation to determine a model exponent.

In this example, we use PyMC to determine the exponent
in a model of the form x^n, where x is the input parameter
and n is the parameter of interest. The data have 10%
of added Gaussian noise.
"""

import numpy as np
import pymc as mc

# Data
inputs = np.array([1, 2, 3, 4, 5])
data = np.array([1, 4, 9, 16, 25])

# Add 10% Gaussian noise to data
data = data + data * 0.10 * np.random.normal(size=len(data))

# Priors
theta = mc.Uniform('theta', lower=[0], upper=[5], value=[2.5])
sigma = mc.Uniform('sigma', lower=[0], upper=[10], value=[1])

# Deterministic node for y_mean from model
@mc.deterministic
def y_mean(theta=theta, inputs=inputs):
    return inputs**theta

# Stochastic node set to observed (data)
y_obs = mc.Normal('y_obs', value=data, mu=y_mean,
                  tau=sigma**-2, observed=True)

# Generate model
m = mc.MCMC([theta,sigma])

# Configure and run MCMC simulation
m.sample(iter=10000, burn=5000, thin=10)

# Plot resulting distributions and convergence diagnostics
mc.Matplot.plot(m, format='pdf',
                path='./Figures',
                common_scale=False)

# Display results
m.summary()
