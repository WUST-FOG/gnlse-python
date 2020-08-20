gnlse-python
============

gnlse-python is a Python set of scripts for solving Generalized Nonlinear
Schrodinger Equation. It is one of the WUST-FOG students projects developed by
`Fiber Optics Group, WUST <http://www.fog.pwr.edu.pl/>`_.

Installation
------------

 1. Create a virtual environment using ``python -m venv gnlse`` or ``conda``.
 2. Activate it:

    ``. gnlse/bin/activate``

 3. Clone the GitHub repository:

    ``git clone https://github.com/WUST-FOG/gnlse-python.git``

 4. Install the requirements:

    ``pip install -r requirements.txt``

 5. Install the package:

    ``pip install .``

    or add the relevant path to your ``PYTHONPATH`` enviroment variable.

Usage
-----

We provide some example Python scripts in the ``examples`` subdirectory. For
instance, running ``test_Dudley.py`` demonstrates supercontinuum generation in
an optical fiber using three different input pulse envelopes.

::

  cd gnlse-python/examples
  python test_Dudley.py

A visualisation, pictured in the screenshot below, is then displayed.

.. image:: _static/supercontinuum_3pulses.png


Major features
--------------

  * **A modular design.**

    The main core of the module is derived from the RK4IP MATLAB script written
    by J. C. Travers, H. Frosz and J. M. Dudley, published [DT10]_.

  * Support for three Raman response functions: ``blowwood`` [BW89]_,
    ``linagrawal`` [LA06]_ and ``hollenbeck`` [HC02]_.
  * Support for two dispersion operators: calculated from a Taylor expansion
    and calculated from effective refractive indices.
  * A number of example scripts in the ``examples`` subdirectory:

     * ``plot_input_pulse.py``, plotting various input impulse envelopes,
     * ``plot_Raman_response.py``, plotting supported Raman response functions
       in the time domain,
     * ``test_3rd_order_soliton.py``, demonstrating the evolution of spectral
       and temporal characteristics of a third-order soliton,
     * ``test_dispersion.py``, an example of supercontinuum generation using
       different dispersion operators,
     * ``test_Dudley``, an example of supercontinuum generation using different
       input impulse envelopes,
     * ``test_gvd``, showing impulse broadening due to group velocity
       dispersion,
     * ``test_import_export.py``, an example of saving and loading simulation
       results to and from a \*.mat file.
     * ``test_raman.py``, showing solition fission in case for different Raman
       responses,
     * ``test_spm``, an example of self-phase modulation,
     * ``test_spm+gvd``, demonstrating generation of a first-order soliton.
       

Release history
---------------

v1.0.0 was released on August 13, 2020. The master branch works with
**Python 3.7.**

=======  ===============  =====================================================
Version  Date             Notes
=======  ===============  =====================================================
1.0.0    August 13, 2020  * The first proper release
                          * CHANGE: Complete documentation and code.
=======  ===============  =====================================================

Authors
-------

  * `Adam Pawłowski <https://github.com/adampawl>`_
  * `Paweł Redman <https://redman.xyz/>`_
  * `Daniel Szulc <http://szulc.xyz/>`_
  * Magda Zatorska
  * `Sylwia Majchrowska <https://majsylw.netlify.app/>`_
  * `Karol Tarnowski <http://www.if.pwr.wroc.pl/~tarnowski/>`_

Acknowledgements
----------------

*gnlse-python* is an open-source project, contributed to by researchers,
engineers and students of the Wrocław University of Science and Technology, as
part of Fiber Optic Group's nonlinear simulation projects. The Python code was
partially based on MATLAB code, published in [DT10], available at
http://scgbook.info/.

Contributing
------------

Pull requests are welcome. For major changes, please open an issue first to
discuss what you would like to change.

Please make sure to update examples and tests as appropriate.

License
-------

This project is licensed under the terms of the `MIT License
<https://choosealicense.com/licenses/mit/>`_.

Code reference
--------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   reference

References
----------

.. [DT10] Dudley, J., & Taylor, J. (Eds.). (2010). Supercontinuum Generation
   in Optical Fibers. Cambridge: Cambridge University Press.
   doi:10.1017/CBO9780511750465
.. [BW89] Blow, K. J., & Wood, D. (1989). Theoretical description of transient
   stimulated Raman scattering in optical fibers. IEEE Journal of Quantum
   Electronics, 25(12), 2665–2673. https://doi.org/10.1109/3.40655
.. [LA06] Lin, Q., & Agrawal, G. P. (2006). Raman response function for silica
   fibers. Optics Letters, 31(21), 3086. https://doi.org/10.1364/ol.31.003086
.. [HC02] Hollenbeck, D., & Cantrell, C. D. (2002). Multiple-vibrational-mode
   model for fiber-optic Raman gain spectrum and response function. Journal of
   the Optical Society of America B, 19(12), 2886.
   https://doi.org/10.1364/josab.19.002886
