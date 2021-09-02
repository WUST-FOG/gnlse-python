"""Amplitude envelopes of different impulses

This module contains functions drawing envelopes of various impulses:
hyperbolic secant, gaussian and lorentzian.

"""

import numpy as np
from scipy import interpolate


class Envelope(object):
    def A(T):
        raise NotImplementedError()


class SechEnvelope(Envelope):
    """Amplitude envelope of hyperbolic secant impulse.

    Attributes
    ----------
    Pmax : float
        Peak power, [W].
    FWHM : float
        Pulse duration Full-Width Half-Maximum.
    """

    def __init__(self, Pmax, FWHM):
        self.name = 'Hyperbolic secant envelope'
        self.Pmax = Pmax
        self.FWHM = FWHM

    def A(self, T):
        """

        Parameters
        ----------
        T : ndarray, (n, )
            Time vector

        Returns
        -------
        ndarray, (n, )
            Amplitude envelope of hyperbolic secant impulse in time.
        """
        m = 2 * np.log(1 + np.sqrt(2))
        return np.sqrt(self.Pmax) * 2 / (np.exp(m * T / self.FWHM) +
                                         np.exp(-m * T / self.FWHM))


class GaussianEnvelope(Envelope):
    """Amplitude envelope of gaussian impulse.

    Attributes
    ----------
    Pmax : float
        Peak power [W].
    FWHM : float
        Pulse duration Full-Width Half-Maximum.
    """

    def __init__(self, Pmax, FWHM):
        self.name = 'Gaussian envelope'
        self.Pmax = Pmax
        self.FWHM = FWHM

    def A(self, T):
        """

        Parameters
        ----------
        T : ndarray, (n, )
            Time vector.

        Returns
        -------
        ndarray, (n, )
            Amplitude envelope of gaussian impulse in time.
        """
        m = 4 * np.log(2)
        return np.sqrt(self.Pmax) * np.exp(-m * .5 * T**2 / self.FWHM**2)


class LorentzianEnvelope(Envelope):
    """Amplitude envelope of lorentzian impulse.

    Attributes
    ----------
    Pmax : float
        Peak power [W].
    FWHM : float
        Pulse duration Full-Width Half-Maximum.
    """

    def __init__(self, Pmax, FWHM):
        self.name = 'Lorentzian envelope'
        self.Pmax = Pmax
        self.FWHM = FWHM

    def A(self, T):
        """

        Parameters
        ----------
        T : ndarray, (n, )
            Time vector.

        Returns
        -------
        ndarray, (n, )
            Amplitude envelope of lorentzian impulse in time.
        """
        m = 2 * np.sqrt(np.sqrt(2) - 1)
        return np.sqrt(self.Pmax) / (1 + (m * T / self.FWHM)**2)


class CWEnvelope(Envelope):
    """Amplitude envelope of continious wave
    with or without some temporal noise.

    Attributes
    ----------
    Pmax : float
        Peak power [W].
    Pn : float, optional
        Peak power for noise [W].
    """

    def __init__(self, Pmax, Pn=0):
        self.name = 'Continious Wave'
        self.Pmax = Pmax
        self.Pn = Pn

    def A(self, T):
        """

        Parameters
        ----------
        T : ndarray, (n, )
            Time vector.

        Returns
        -------
        ndarray, (n, )
            Amplitude envelope of continious wave in time.
        """
        cw = np.fft.ifft(np.sqrt(self.Pmax) * np.ones(np.size(T)))
        noise = 0
        if self.Pn:
            noise = np.sqrt(self.Pn
                            ) * np.exp(
                1j * 2 * np.pi * np.random.rand(np.size(T)))
        return np.fft.fft(cw + noise)


class RawDataEnvelope(Envelope):
    """Amplitude envelope of impulse
    reconstructed from experimantal data.

    Attributes
    ----------
    time : ndarray, (n, )
        Time vector.
    intensity : ndarray, (n, )
        Time vector.
    phase : ndarray, (n, )
        Peak power [W].
    energy : float
        Enery of impulse [J].
    """

    def __init__(self, time, intensity, phase, energy):
        self.name = 'Raw Data Envelope'
        self.time = time
        self.intensity = intensity
        self.phase = phase
        self.energy = energy

    def A(self, T):
        """

        Parameters
        ----------
        T : ndarray, (n, )
            Time vector.

        Returns
        -------
        ndarray, (n, )
            Amplitude envelope of continious wave in time.
        """
        # interpolation of real data
        intensity = interpolate.interp1d(self.time,
                                         self.intensity,
                                         kind='cubic',
                                         fill_value="extrapolate")
        fi = interpolate.interp1d(self.time,
                                  self.phase,
                                  kind='cubic',
                                  fill_value="extrapolate")

        A = np.sqrt(intensity(T)) * np.exp(1j * fi(T))

        # normalization of power
        E = np.trapz(T, np.abs(A)**2)

        return A * np.sqrt(self.energy / E)
