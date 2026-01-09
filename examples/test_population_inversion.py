import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import gnlse_main
from copy import deepcopy
if __name__ == '__main__':
    setup = gnlse_main.gnlse.GNLSESetup()

    # Numerical parameters
    # number of grid time points
    setup.resolution = 2**13
    # time window [ps]
    setup.time_window = 12.5
    # number of distance points to save
    setup.z_saves = 400
    # relative tolerance for ode solver
    setup.rtol = 1e-6
    # absoulte tolerance for ode solver
    setup.atol = 1e-6

    # Physical parameters
    # Central wavelength [nm]
    setup.wavelength = 1030
    # Nonlinear coefficient [1/W/m]
    setup.nonlinearity = 0
    # Dispersion: derivatives of propagation constant at central wavelength
    # n derivatives of betas are in [ps^n/m]
    betas = np.array([2.3e-2,58*1e-6])
    # Input pulse: pulse duration [ps]
    tFWHM = 0.5
    # for dispersive length calculation
    t0 = tFWHM / 2 / np.log(1 + np.sqrt(2))

    # Fiber length [m]
    setup.fiber_length = 1
    # Type of pulse:  gaussian
    pulseEnergy = 20e-12  #desired pulse energy in joules
    peakPowerGaussian = 0.94 * (pulseEnergy/(tFWHM*1e-12))
    setup.pulse_model = gnlse_main.GaussianEnvelope(peakPowerGaussian, tFWHM)
    dt = np.linspace(-setup.time_window/2,setup.time_window/2,setup.resolution)[1]-np.linspace(-setup.time_window/2,setup.time_window/2,setup.resolution)[0]
    print(f"Pulse energy: {np.trapezoid(np.square(np.abs(setup.pulse_model.A(np.linspace(-setup.time_window/2,setup.time_window/2,setup.resolution)))),dx=dt*1e-12)}")
    # Loss coefficient [dB/m]
    loss = 0.5/1000
    # Type of dyspersion operator: build from Taylor expansion
    #Set parameters necessary for gain modelling
    gain_medium_radius = (11.6e-6)*0.5
    fiber_area = np.pi * (gain_medium_radius**2)
    dopant_concentration = (5e25)
    emission = pd.read_csv(r"data\emissionCS.csv") #get absorption and emission cross sections from csv
    absorption = pd.read_csv(r"data\absorptionCS.csv")
    lifetime = 0.85e-3
    repetition_rate = 1e6 #10kHz
    pump_power = 5 #pump power in watts

    setup.self_steepening = True
    setup.active_fiber = True


    setup.dispersion_model = gnlse_main.DispersionFiberFromTaylorWithGain(loss,betas,fiber_area,dopant_concentration,emission,absorption,lifetime,pump_power,repetition_rate=repetition_rate)

    solver = gnlse_main.gnlse.GNLSE(setup)
    
    #test in dispersion operator
    solution = solver.run()

    gnlse_main.plot_delay_vs_distance(solution)
    plt.figure(figsize=(10,3))
    gnlse_main.visualization.plot_energy_vs_distance(solution)
    plt.figure()
    gnlse_main.plot_wavelength_vs_distance(solution,[1000,1100])
    plt.figure()
    plt.plot(solver.n2log["z"],solver.n2log["n2"])
    plt.xlabel("z")
    plt.ylabel("$n_2$")
    plt.ylim(0,1)
    plt.figure()
    plt.plot(solver.n2log["z"],solver.n2log["E"])
    plt.show()
    
