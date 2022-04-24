"""Nonlinearity coefficient in optical fibres.

Based on delivered frequency vector and effictive mode areas
script calculates nonlinear coefficient in
frequency domain.

"""
import numpy as np
from scipy import interpolate

from gnlse.common import c


class Nonlinearity(object):
    def gamma(V):
        """Calculate nonlinear coefficient
        for given frequency grid created during simulation

        Parameters
        ----------
        V : ndarray, (N)
            Frequency vector

        Returns
        -------
        ndarray, (N)
            Nonlinear coefficient in frequency domain
        """

        raise NotImplementedError('Nonlinearity not implemented')


class NonlinearityFromEffectiveArea(Nonlinearity):
    """Calculate the nonlinearity coefficient in
    frequency domain based on modified gnlse example form
    J. Lægsgaard, "Mode profile dispersion in the generalized
    nonlinear Schrödinger equation,"
    Opt. Express 15, 16110-16123 (2007).

    Attributes
     ----------
    neff : ndarray (N)
        Effective refractive index
    Aeff : ndarray (N)
        Effective mode area
    lambdas : ndarray (N)
        Wavelength corresponding to refractive index
    central_wavelength : float
        Wavelength corresponding to pump wavelength in nm
    n2 : float
        Nonlinear index of refraction in m^2/W
    """

    def __init__(self, neff, Aeff, lambdas, central_wavelength,
                 n2=2.7e-20, neff_max=None):
        # refractive indices
        self.neff = neff
        # efective mode area in m^-2
        self.Aeff = Aeff
        # wavelengths for neffs in nm
        self.lambdas = lambdas
        # central frequency in 1/ps [THz]
        self.w0 = (2.0 * np.pi * c) / central_wavelength
        # nonlinear index of refraction in m^2/W
        self.n2 = n2
        # maximum (artificial) value of neff
        self.neff_max = neff_max

    def gamma(self, V):
        # Central frequency [1/ps = THz]
        omega = 2 * np.pi * c / self.lambdas
        Omega = V + self.w0

        # Extrapolate effective mode area for a frequency vector
        Aeff_interp = interpolate.interp1d(omega,
                                           self.Aeff,
                                           kind='cubic',
                                           fill_value="extrapolate")
        # Extrapolate effective mode area for a frequency vector
        neff_interp = interpolate.interp1d(omega,
                                           self.neff,
                                           kind='cubic',
                                           fill_value="extrapolate")

        # Refractive index
        neff = neff_interp(Omega)
        if self.neff_max is not None:
            neff[Omega < omega[-1]] = self.neff_max
        # and at central frequency
        n0 = neff_interp(self.w0)
        # Efective mode area
        Aeff = Aeff_interp(Omega)
        if self.neff_max is not None:
            Aeff[Omega < omega[-1]] = max(self.Aeff)
        # and at central frequency [1/m^2]
        Aeff0 = Aeff_interp(self.w0)

        gamma = self.n2 * self.w0 \
            * n0 / c / 1e-9 / neff / np.sqrt(Aeff * Aeff0)
        return gamma, np.power(Aeff0 / Aeff, 1. / 4)
