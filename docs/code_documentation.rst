GNLSE package documentation
===========================

Impulse envelopes
-----------------

This module allows one to model proper input envelope as the given initial
conditions to solve Generalized Nonlinear Schrodiner Equation (GNLSE).

.. autosummary::

   gnlse.SechEnvelope
   gnlse.GaussianEnvelope
   gnlse.LorentzianEnvelope

GNLSE model
-----------

This part of the module is its core, and it implements the split-step Fourier
method to solve the GNLSE.

.. autosummary::

   gnlse.GNLSESetup
   gnlse.GNLSE
   gnlse.Solution

Dispersion operators
--------------------

Package supports two dispersion operators: calculated from a Taylor expansion
and calculated from effective refractive indices.

.. autosummary::

   gnlse.DispersionFiberFromTaylor
   gnlse.DispersionFiberFromInterpolation

Raman responses
---------------

Package supports three Raman response functions: ``blowwood`` [BW89]_,
``linagrawal`` [LA06]_ and ``hollenbeck`` [HC02]_.

.. autosummary::

   gnlse.raman_blowwood
   gnlse.raman_holltrell
   gnlse.raman_linagrawal

Visualisation
-------------

Various plotting functions for visualizing GNLSE simulations using Matplotlib
library are prepared.

.. autosummary::

   gnlse.plot_wavelength_vs_distance
   gnlse.plot_delay_vs_distance
   gnlse.quick_plot

Importing and exporting
-----------------------

The following functions allow one to read and write data as \\*.mat files.

.. autosummary::

   gnlse.read_mat
   gnlse.write_mat
