"""
Example: self-phase modulation on 3.5*pi nonlinear length
for gaussian pulse as in Chapter 4 of Nonlinear Fiber Optics.

Interface based on MATLAB code published in
'Supercontinuum Generation in Optical Fibers'
by J. M. Dudley and J. R. Taylor, available at http://scgbook.info/.
"""

import numpy as np
import gnlse
import matplotlib.pyplot as plt


if __name__ == '__main__':
    setup = gnlse.gnlse.GNLSESetup()

    # Numerical parameters
    ###########################################################################
    # number of grid time points
    setup.resolution = 2**13
    # time window [ps]
    setup.time_window = 12.5
    # number of distance points to save
    setup.z_saves = 200
    # relative tolerance for ode solver
    setup.rtol = 1e-6
    # absoulte tolerance for ode solver
    setup.atol = 1e-6

    # Physical parameters
    ###########################################################################
    # Central wavelength [nm]
    setup.wavelength = 835
    # Nonlinear coefficient [1/W/m]
    setup.nonlinearity = 0.11
    # Dispersion: derivatives of propagation constant at central wavelength
    # n derivatives of betas are in [ps^n/m]
    betas = np.array([0])
    # Input pulse: pulse duration [ps]
    tFWHM = 0.050

    ###########################################################################
    # Input pulse: peak power [W]
    power = 1  # value can be choosen arbitrarily
    # Non-linear length for given nonlinearity and power
    LNL = 1 / (power * setup.nonlinearity)
    # Fiber length [m]
    setup.fiber_length = 3.5 * np.pi * LNL
    # Type of pulse:  gaussian
    setup.pulse_model = gnlse.GaussianEnvelope(power, tFWHM)
    # Loss coefficient [dB/m]
    loss = 0
    # Type of dyspersion operator: build from Taylor expansion
    setup.dispersion_model = gnlse.DispersionFiberFromTaylor(loss, betas)

    # Type of Ramman scattering function: None (default)
    # Selftepening: not accounted
    setup.self_steepening = False

    # Simulation
    ###########################################################################
    solver = gnlse.gnlse.GNLSE(setup)
    solution = solver.run()

    # Visualization
    ###########################################################################
    plt.subplot(1, 2, 1)
    gnlse.plot_wavelength_vs_distance(solution, WL_range=[400, 1400])
    plt.subplot(1, 2, 2)
    gnlse.plot_delay_vs_distance(solution, time_range=[-.25, .25])

    plt.show()
