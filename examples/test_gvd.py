"""
Example: group velocity dispersion on distance of 4 dispersion length
for gaussian pulse as in Chapter 3 of Nonlinear Fiber Optics.

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
    setup.nonlinearity = 0.
    # Dispersion: derivatives of propagation constant at central wavelength
    # n derivatives of betas are in [ps^n/m]
    betas = np.array([-11.830e-3])
    # Input pulse: pulse duration [ps]
    tFWHM = 0.050
    t0 = tFWHM / 2 / np.sqrt(np.log(2))  # for dispersive length calculations

    ###########################################################################
    # Dispersive length
    LD = t0 ** 2 / np.abs(betas[0])
    # Input pulse: peak power [W]
    power = 1  # value can be choosen arbitrarily
    # Fiber length [m]
    setup.fiber_length = 4 * LD
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
    gnlse.plot_wavelength_vs_distance(solution, WL_range=[780, 900])
    plt.subplot(1, 2, 2)
    gnlse.plot_delay_vs_distance(solution, time_range=[-.5, .5])

    plt.show()
