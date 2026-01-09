"""Dispersion operator in optical fibres.

Based on delivered frequency vector and damping indexes
script calculates linear dispersion operator in
frequency domain.

"""
import numpy as np
import math
import pandas as pd
from scipy import interpolate

from gnlse_main.common import c
from gnlse_main.common import hplanck

class Dispersion(object):
    """
    Attributes
    -----------
    loss : float
        Loss factor [dB/m]
    """

    def __init__(self, loss):
        self.loss = loss

    def D(V):
        """Calculate linear dispersion operator
        for given frequency grid created during simulation

        Parameters
        ----------
        V : ndarray, (N)
            Frequency vector

        Returns
        -------
        ndarray, (N)
            Linear dispersion operator in frequency domain
        """

        raise NotImplementedError('Dispersion not implemented')

    def calc_loss(self):
        """Calculate damping
        for given frequency grid created during simulation
        """
        self.alpha = np.log(10**(self.loss / 10))


class DispersionFiberFromTaylor(Dispersion):
    """Calculates the dispersion in frequency domain

    Attributes
     ----------
    loss : float
        Loss factor [dB/m]
    betas : ndarray (N)
        Derivatives of constant propagations at pump wavelength
        [ps^2/m, ..., ps^n/m]
    """

    def __init__(self, loss, betas):
        self.loss = loss
        self.betas = betas

    def D(self, V):
        # Damping
        self.calc_loss()
        # Taylor series for subsequent derivatives
        # of constant propagation
        B = sum(beta / math.factorial(i + 2) * V**(i + 2)
                for i, beta in enumerate(self.betas))
        L = 1j * B - self.alpha / 2
        return L

class DispersionFiberFromTaylorWithGain(Dispersion):
    #under development - not yet functional
    #basic version - gain is applied equally at all points - no time dependence on measuring gain as intensities are averaged for now
    """Calculates the dispersion in frequency domain with the gain operator

    Attributes
     ----------
    loss : float
        Loss factor [dB/m]
    betas : ndarray (N)
        Derivatives of constant propagations at pump wavelength
        [ps^2/m, ..., ps^n/m]
    """

    def __init__(self, loss, betas,fiber_area,dopant_concentration,emission,absorption,lifetime,pump_power=None,overlap_pump=1,overlap_signal=1,repetition_rate=1e6):
        self.loss = loss
        self.betas = betas

        #active fiber parameters
        self.fiber_area = fiber_area
        self.dopant_concentration = dopant_concentration # if None, fiber is passive, otherwise model gain, this is the concentration per unit volume * dz, so N_total = dopant_concentration * fiber_area
        self.lifetime =lifetime
        self.pump_power = pump_power #assumed to be constant for now
        self.AW = None
        self.v = None
        self.emission = emission #emission and absorption contain pandas dataframes with wavelength in nm and cross sections in m^2
        self.absorption = absorption
        self.overlap_pump = overlap_pump
        self.overlap_signal = overlap_signal
        self.repetition_rate = repetition_rate #defaults to 1MHz
        self.dt = None
        self.N2Total = None
        self.NT = None
    def N2(self):
        if type(self.AW) == bool:
            raise TypeError("Amplitude spectrum was not defined, cannot compute population inversion. D.AW must not be None.")
        Ip = self.pump_power/self.fiber_area
        Isw = np.square(np.abs(self.AW))
        #first we find the pulse energy - integrate Isw over v
        At = np.fft.ifft(self.AW)
        pulse_energy = np.trapezoid(np.square(np.abs(At)),dx=(self.dt*1e-12))
        self.pulse_energy_log = pulse_energy
        Ps = pulse_energy * self.repetition_rate #average signal power
        Is = Ps/self.fiber_area
        #set central frequency as average weighted by intensity
        central_frequency = np.average(self.v,weights=Isw)
        #get as wavelength in nm
        central_wavelength = (c/central_frequency)*1e12
        #now we find the cross section at central_frequency
        pump_wavelength = 975 #leaving this constant for Yb amplifier
        pump_frequency = c/(pump_wavelength *1e-12)
        em_cross_section_signal = self.emission[r"cross section(m^2)"][(np.abs(self.emission["wavelength(nm)"]-central_wavelength)).argmin()] #cross section @ closest wavelength
        abs_cross_section_signal = self.absorption[r"cross section(m^2)"][(np.abs(self.absorption["wavelength(nm)"]-central_wavelength)).argmin()]
        em_cross_section_pump = self.emission[r"cross section(m^2)"][(np.abs(self.emission["wavelength(nm)"]-pump_wavelength)).argmin()] 
        abs_cross_section_pump = self.absorption[r"cross section(m^2)"][(np.abs(self.absorption["wavelength(nm)"]-pump_wavelength)).argmin()]

        #Now compute R and W values
        R12 = (abs_cross_section_pump*Ip)/(hplanck*pump_frequency)
        R21 = (em_cross_section_pump*Ip)/(hplanck*pump_frequency)
        W12 = (abs_cross_section_signal*Is)/(hplanck*central_frequency)
        W21 = (em_cross_section_signal*Is)/(hplanck*central_frequency)

        #finally compute N2
        numerator = R12 + W12
        denominator = R12 + W12 + R21 + W21 + (1/self.lifetime)
        n2 = numerator/denominator
        self.N2Total = n2*(self.dopant_concentration)
        self.NT = self.dopant_concentration
        return n2*self.dopant_concentration #returns the absolute number of excited Yb atoms
    def SetFrequency(self,v):
        self.v = v
        self.wavelengths = (c/v)*1e12
        self.sigma_a = np.array([self.absorption[r"cross section(m^2)"][(np.abs(self.absorption["wavelength(nm)"] - wavelength)).argmin()] for wavelength in self.wavelengths])
        self.sigma_e = np.array([self.emission[r"cross section(m^2)"][(np.abs(self.emission["wavelength(nm)"] - wavelength)).argmin()] for wavelength in self.wavelengths])

    def CalculateGain(self):
        self.N2()
        n2 = self.N2Total/self.NT
        
        lhs = np.multiply(self.sigma_e, n2)
        rhs = np.multiply(self.sigma_a, np.subtract(1, n2))
        gain = self.NT * np.subtract(lhs,rhs)
        return gain
    
    def D(self, V):
        # Damping
        self.calc_loss()
        # Taylor series for subsequent derivatives
        # of constant propagation
        B = sum(beta / math.factorial(i + 2) * V**(i + 2)
                for i, beta in enumerate(self.betas))
        #compute value of gain function
        gain = self.CalculateGain()
        L = (1j * B) - (self.alpha / 2) + (gain/4) 
        return L

class DispersionFiberFromInterpolation(Dispersion):
    """Calculates the propagation function in frequency domain, using
    the extrapolation method based on delivered refractive indexes
    and corresponding wavelengths. The returned value is a vector
    of dispersion operator.

    Attributes
    -----------
    loss : float
        Loss factor [dB/m]
    neff : ndarray (N)
        Effective refractive index
    lambdas : ndarray (N)
        Wavelength corresponding to refractive index
    central_wavelength : float
        Wavelength corresponding to pump wavelength in nm
    """

    def __init__(self, loss, neff, lambdas, central_wavelength):
        # Loss factor in dB/m
        self.loss = loss
        # refractive indices
        self.neff = neff
        # wavelengths for neffs in [nm]
        self.lambdas = lambdas
        # Central frequency in [1/ps = THz]
        self.w0 = (2.0 * np.pi * c) / central_wavelength

    def D(self, V):
        # Central frequency [1/ps = THz]
        omega = 2 * np.pi * c / self.lambdas
        dOmega = V[1] - V[0]
        Bet = self.neff * omega / c * 1e9  # [1/m]

        # Extrapolate betas for a frequency vector
        fun_interpolation = interpolate.interp1d(omega,
                                                 Bet,
                                                 kind='cubic',
                                                 fill_value="extrapolate")

        B = fun_interpolation(V + self.w0)
        # Propagation constant at central frequency [1/m]
        B0 = fun_interpolation(self.w0)
        # Value of propagation at a lower end of interval [1/m]
        B0plus = fun_interpolation(self.w0 + dOmega)
        # Value of propagation at a higher end of interval [1/m]
        B0minus = fun_interpolation(self.w0 - dOmega)

        # Difference quotient, approximation of
        # derivative of a function at a point [ps/m]
        B1 = (B0plus - B0minus) / (2 * dOmega)

        # Damping
        self.calc_loss()

        # Linear dispersion operator
        L = 1j * (B - (B0 + B1 * V)) - self.alpha / 2
        return L
