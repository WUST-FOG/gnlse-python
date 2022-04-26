"""
Runs a simple simulation, saves it to disk and loads it back for plotting.
"""

import os
import gnlse

if __name__ == '__main__':
    setup = gnlse.GNLSESetup()
    setup.resolution = 2**13
    setup.time_window = 12.5  # ps
    setup.z_saves = 200
    setup.fiber_length = 0.15  # m
    setup.wavelength = 835  # nm
    setup.pulse_model = gnlse.GaussianEnvelope(1, 0.1)

    solver = gnlse.GNLSE(setup)
    solution = solver.run()

    path = 'test.mat'

    solution.to_file(path)
    solution = gnlse.Solution()
    solution.from_file(path)

    gnlse.quick_plot(solution)

    os.remove(path)
