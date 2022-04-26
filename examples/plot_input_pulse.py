"""Calculates envelopes of various pulses and plots them.
Based on the chosen envelopes pulse, the aplitude envelope is
calculated and shown on the graph. There are three
available envelopes pulses models:
hyperbolic secant, gaussian and lorentzian.
"""

import numpy as np
import matplotlib.pyplot as plt

import gnlse

if __name__ == '__main__':
    # time full with half maximum of pulse
    FWHM = 2
    # Time grid [ps]
    T = np.linspace(-2 * FWHM, 2 * FWHM, 1000 * FWHM)
    # peak power [W]
    Pmax = 100

    # Amplitude envelope of gaussina pulse
    A1 = gnlse.GaussianEnvelope(Pmax, FWHM).A(T)
    # Amplitude envelope of hiperbolic secans pulse
    A2 = gnlse.SechEnvelope(Pmax, FWHM).A(T)
    # Amplitude envelope of lorentzian pulse
    A3 = gnlse.LorentzianEnvelope(Pmax, FWHM).A(T)
    # Amplitude envelope of continious wave
    A4 = gnlse.CWEnvelope(Pmax).A(T)

    plt.figure(figsize=(12, 8))
    plt.subplot(1, 2, 1)
    plt.plot(T, A1, label='gauss')
    plt.plot(T, A2, label='sech')
    plt.plot(T, A3, label='lorentz')
    plt.plot(T, A4, label='cw')
    plt.xlabel("Time [ps]")
    plt.ylabel("Amplitude [sqrt(W)]")
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(T, A1**2, label='gauss')
    plt.plot(T, A2**2, label='sech')
    plt.plot(T, A3**2, label='lorentz')
    plt.plot(T, A4**2, label='cw')
    plt.xlabel("Time [ps]")
    plt.ylabel("Power [W]")
    plt.legend()

    plt.show()
