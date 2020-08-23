:orphan:

Integration
===========

This part of the module is its core, and it implements the split-step Fourier
method to solve the Generalized Nonlinear Schrodiner Equation (GNLSE),
which in time domain can be written as

.. math::

   \frac{\partial A(z,T)}{\partial z} = & -\frac{\alpha}{2}A(z,T) - 
   \sum_{k\geq 2} \left(\frac{i^{k-1}}{k!}\beta_k
   \frac{\partial^k A(z,T)}{\partial T^k} \right) + \\
   & + i\gamma\left(1 + \frac{i}{\omega_c} \frac{\partial}{\partial T} \right)
   \left( A(z,T) \int_{-\infty}^{+\infty} R(T') |A(z,T-T')|^2 dT' \right),

where :math:`\alpha` is the attenuation constant, and :math:`\beta_k` are the
higher order dispersion coefficients obtained by a Taylor series expansion of
the propagation constant :math:`\beta(\omega)` around the center frequency
:math:`\omega_c`. The term in second line describes the nonlinear effects -
temporal derivative in this term is responsible for self-steepening
and optical shock formation, whereas the convolution integral describes
the delayed Raman response :math:`R(T')` [H07]_. This form of the GNLSE is
commonly employed for numerical simulations of propagation of pulses in
a nonlinear medium such as optical fiber.

This solver is efficient, thanks to an adaptive-step-size implementation of
the fourth-order Runge-Kutta in the Interaction Picture method (RK4IP),
adapted from [H07]_. Our Python code is partially based on MATLAB code,
published in [DT10]_, available at http://scgbook.info/. The toolbox prepares
integration using SCIPYs ode solver, while the transitions between time and
frequency domains are accomplished using the FFT and iFFT from pyfftw library.

The solver is divided into three parts: specific model setup
(``gnlse.GNLSESetup``), the framework for preparing split-step Fourier
alghoritm (``gnlse.GNLSE``), and class for managing the solution
(``gnlse.Solution``).

.. autoclass:: gnlse.GNLSESetup
.. autoclass:: gnlse.GNLSE
.. autoclass:: gnlse.Solution
