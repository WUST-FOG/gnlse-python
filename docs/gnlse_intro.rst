GNLSE: Nonlinear optics modeling tool for optical fibers
========================================================

gnlse-python is a Python set of scripts for solving Generalized Nonlinear
Schrodinger Equation. It is one of the WUST-FOG students projects developed by
`Fiber Optics Group, WUST <http://www.fog.pwr.edu.pl/>`_.

Complete documentation is available at `https://gnlse.readthedocs.io <https://gnlse.readthedocs.io>`_.

Installation
------------

Using pip
*********

Instal the latest version

``pip install gnlse``

or pick appropriate version as v2.0.0

``pip install gnlse==2.0.0``

From scratch
************

 1. Create a virtual environment using ``python -m venv gnlse`` or ``conda``.
 2. Activate it:

    ``. gnlse/bin/activate``

 3. Clone the GitHub repository:

    ``git clone https://github.com/WUST-FOG/gnlse-python.git``

 4. Install the package with all requirements:

    ``pip install .``

    or add the relevant path to your ``PYTHONPATH`` enviroment variable.

Dependencies
************

The following Python packages are required to install gnlse module. During
instalation of package the latest version of each of listed below package will
automatically be installed if missing:

::

  matplotlib>=2.2.2
  numpy>=1.14.3
  scipy>=1.1.0
  pyfftw>=0.10.0
  hdf5storage>=0.1.15
  tqdm>=4.11.2

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

.. toctree::
   :maxdepth: 2
   :caption: Examples:

   examples/index

More examples can be found in the `examples subdirectory 
<https://github.com/WUST-FOG/gnlse-python/tree/master/examples>`_.

Major features
--------------

  * **A modular design**: the solver framework was decomposed into different
    components and one can easily construct a customized simulations by
    accounting different physical phenomena, ie. self stepening,
    Raman response.

    The main core of the module is derived from the RK4IP MATLAB script
    written by J. C. Travers, H. Frosz and J. M. Dudley, published [DT10]_.

  * Support for three Raman response functions: ``blowwood`` [BW89]_,
    ``linagrawal`` [LA06]_ and ``hollenbeck`` [HC02]_.
  * Support for two dispersion operators: calculated from a Taylor expansion
    and calculated from effective refractive indices.
  * A number of example scripts in the ``examples`` subdirectory:

     * ``plot_input_pulse.py``, plotting various input pulse envelopes,
     * ``plot_Raman_response.py``, plotting supported Raman response functions
       in the time domain,
     * ``test_3rd_order_soliton.py``, demonstrating the evolution of spectral
       and temporal characteristics of a third-order soliton,
     * ``test_dispersion.py``, an example of supercontinuum generation using
       different dispersion operators,
     * ``test_nonlinearity.py``, an example of soliton fission using
       different GNLSE and Modified GNLSE accounting mode profile dispersion,
       (take into account mode profile dispersion),  
     * ``test_Dudley.py``, an example of supercontinuum generation using
       different input pulse envelopes,
     * ``test_gvd.py``, showing pulse broadening due to group velocity
       dispersion,
     * ``test_import_export.py``, an example of saving and loading simulation
       results to and from a \*.mat file,
     * ``test_raman.py``, showing solition fission in case for different Raman
       responses,
     * ``test_spm.py``, an example of self-phase modulation,
     * ``test_spm+gvd.py``, demonstrating generation of a first-order soliton.
       

Release information
-------------------

v2.0.0 was released on April 26, 2022. The main branch works with
**Python 3.7.**

=======  ================= ====================================================
Version  Date              Notes
=======  ================= ====================================================
2.0.0    April 26, 2022    * CHANGE: Code refactor - rename modules
                           * FIX: Fixed extrapolation for nonlinear coefficient
1.1.3    February 13, 2022 * FIX: Fix scaling for interpolated dispersion
1.1.2    August 30, 2021   * ADD: Continious wave envelope
                           * FIX: Shift scalling data for nonlinear coefficient
1.1.1    August 28, 2021   * CHANGE: Minor bug fix with scaling
                           * CHANGE: Few minor changes in the documentation
1.1.0    August 21, 2021   * Modified-GNLSE extension
                           * CHANGE: Code refactor - relocate attribiutes
1.0.0    August 13, 2020   * The first proper release
                           * CHANGE: Complete documentation and code.
=======  ================= ====================================================

Authors
*******

  * `Adam Pawłowski <https://github.com/adampawl>`_
  * `Paweł Redman <https://redman.xyz/>`_
  * `Daniel Szulc <http://szulc.xyz/>`_
  * `Magda Zatorska <https://github.com/magdazatorska>`_
  * `Sylwia Majchrowska <https://majsylw.netlify.app/>`_
  * `Karol Tarnowski <http://www.if.pwr.wroc.pl/~tarnowski/>`_

Citation
********

If you use a code please `cite <https://arxiv.org/pdf/2110.00298.pdf>`_ us:

Paragraph ... ::

    @misc{redman2021gnlsepython,
          title={gnlse-python: Open Source Software to Simulate Nonlinear Light Propagation In Optical Fibers}, 
          author={Paweł Redman and Magdalena Zatorska and Adam Pawłowski and Daniel Szulc and Sylwia Majchrowska and Karol Tarnowski},
          year={2021},
          eprint={2110.00298},
          archivePrefix={arXiv},
          primaryClass={physics.optics}
    }

Contributing
************

Pull requests are welcome. For major changes, please open an issue first to
discuss what you would like to change.

Please make sure to update examples and tests as appropriate.

Acknowledgements
****************

**gnlse-python** is an open-source project, contributed to by researchers,
engineers and students of the Wrocław University of Science and Technology, as
part of Fiber Optic Group's nonlinear simulation projects. The Python code was
partially based on MATLAB code, published in [DT10]_, available at
http://scgbook.info/.

License
*******

This project is licensed under the terms of the `MIT License
<https://choosealicense.com/licenses/mit/>`_.
