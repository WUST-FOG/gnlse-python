"""Calculates different Raman responses , based on the
chosen Raman model, the response is calculated.
There are three available Raman reponse models for
silica optical fibers:
- based on K. J. Blow and D. Wood model,
- based on Dawn Hollenbeck and Cyrus D. Cantrell model,
- based on Q. Lin and Govind P. Agrawal model.

Example
-------
By applying different index of raman response for
silica fibers, different model is chosen.
Function takes the time vector and calculates the
Raman response based on the chosen model.

"""

import numpy as np


def raman_blowwood(T):
    """Raman scattering function for silica optical fibers, based on K. J. Blow
    and D. Wood model.

    Parameters
    ----------
    T : float
       Time vector.

    Returns
    -------
    fr : float
       Share of Raman response.
    RT : ndarray
       Vector representing Raman response.

    """

    # Raman response [arbitrary units]
    fr = 0.18
    # Adjustable parameters used to fit the actual Raman gain spectrum [ps]
    tau1 = 0.0122
    tau2 = 0.032
    # Raman response function
    ha = (tau1**2 + tau2**2) / tau1 / (tau2**2) * np.exp(-T / tau2) * np.sin(
        T / tau1)
    RT = ha

    RT[T < 0] = 0

    return fr, RT


def raman_holltrell(T):
    """Raman scattering function for silica optical fibers, based on Dawn
    Hollenbeck and Cyrus D. Cantrell model.

    Parameters
    ----------
    T : float
        Time vector.

    Returns
    -------
    fr : float
       Share of Raman response.
    RT : ndarray
       Vector representing Raman response.

    """

    # Raman response [arbitrary units]
    fr = 0.2
    # The speed of light [nm/ps]
    c = 299792458 * 1e-3

    # Component position  [1/cm]
    CP = np.array([
        56.25, 100.0, 231.25, 362.5, 463.0, 497.0, 611.5, 691.67, 793.67,
        835.5, 930.0, 1080.0, 1215.0
    ])
    # Peak intensity (amplitude)
    A = np.array([
        1.0, 11.40, 36.67, 67.67, 74.0, 4.5, 6.8, 4.6, 4.2, 4.5, 2.7, 3.1, 3.0
    ])
    # Gaussian FWHM [1/cm]
    Gauss = np.array([
        52.10, 110.42, 175.00, 162.50, 135.33, 24.5, 41.5, 155.00, 59.5, 64.3,
        150.0, 91.0, 160.0
    ])
    # Lorentzian FWHM [1/cm]
    Lorentz = np.array([
        17.37, 38.81, 58.33, 54.17, 45.11, 8.17, 13.83, 51.67, 19.83, 21.43,
        50.00, 30.33, 53.33
    ])

    w = 1e-7 * 2 * np.pi * c * CP
    L = 1e-7 * np.pi * c * Gauss
    gamma = 1e-7 * np.pi * c * Lorentz

    # RT = A * np.exp(-gamma * T) * np.exp((-L ** 2 * T ** 2 )/ 4) * np.sin(
    #      w * T)   # rozszerzenie pośrednie
    # RT = A * np.exp((-(L ** 2) * T ** 2) / 4) * np.sin(w * T) # nonuniform
    # RT = A * np.sin(w * T) * np.exp(-gamma * T)               # unform

    RT = np.zeros_like(T)

    for i in range(len(A)):
        RT += A[i] * np.exp(-gamma[i] * T) * np.exp(
            (-L[i]**2 * T**2) / 4) * np.sin(w[i] * T)

    RT[T < 0] = 0
    dt = T[1] - T[0]
    RT = RT / (np.sum(RT) * dt)

    return fr, RT


def raman_linagrawal(T):
    """Raman scattering function for silica optical fibers, based on Q. Lin
    and Govind P. Agrawal model.

    Parameters
     ----------
    T : float
        Time vector.

    Returns
    -------
    fr : float
       Share of Raman response.
    RT : ndarray
       Vector representing Raman response.

    """

    # Raman response [arbitrary units]
    fr = 0.245
    # Adjustable parameters used to fit the actual Raman gain spectrum [ps]
    tau1 = 0.0122
    tau2 = 0.032
    taub = 0.096
    # Fractional contribution of the anisotropic reponse to the total Raman
    # response
    fb = 0.21
    fc = 0.04
    # Fractional contribution of the isotropic reponse to the total Raman
    # response
    fa = 1 - fb - fc
    # Anisotropic Raman response
    ha = (tau1**2 + tau2**2) / tau1 / (tau2**2) * np.exp(-T / tau2) * np.sin(
        T / tau1)
    # Izotropic Raman respons
    hb = (2 * taub - T) / (taub**2) * np.exp(-T / taub)
    # Total Raman response
    RT = (fa + fc) * ha + fb * hb

    RT[T < 0] = 0

    return fr, RT


if __name__ == '__main__':
    """Calculates different Raman responses and plots them.
    Based on the chosen Raman model, the response is
    calculated and shown on the graph. There are three
    available Raman reponse models.
    """
    import matplotlib.pyplot as plt
    # Initial paremeters
    ###########################################################################
    # Number of grid points
    n = 2**13
    # Time window width [ps]
    twidth = 12.5
    # The speed of light [nm/ps]
    c = 299792458 * 1e-3
    # Central wavelength [nm]
    wavelength = 835
    # Central frequency [THz]
    w0 = (2 * np.pi * c) / wavelength
    # Time grid [ps]
    T = np.linspace(-twidth / 2, twidth / 2, n)

    # Blowwood Raman response
    fr, RT1 = raman_blowwood(T)
    RT1 = RT1 / np.max(RT1)
    # Linagrawal Raman response
    fr2, RT2 = raman_linagrawal(T)
    RT2 = RT2 / np.max(RT2)
    # Holltrell Raman response
    fr3, RT3 = raman_holltrell(T)
    RT3 = RT3 / np.max(RT3)

    plt.plot(T, RT1, label="Blowwod")
    plt.plot(T, RT2, label="Linagrawal")
    plt.plot(T, RT3, label="Holltrell")

    plt.xlim(-0.025, 1)
    plt.ylabel("Raman Response [AU]")
    plt.xlabel("Time Grid [ps]")

    plt.legend()

    plt.show()
