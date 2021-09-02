![](https://github.com/WUST-FOG/gnlse-python/workflows/CI/badge.svg)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5377289.svg)](https://doi.org/10.5281/zenodo.5377289)

# gnlse-python

gnlse-python is a Python set of scripts for solving
Generalized Nonlinear Schrodringer Equation. It is one of the WUST-FOG students
projects developed by [Fiber Optics Group, WUST](http://www.fog.pwr.edu.pl/).

Complete documentation is available at
[https://gnlse.readthedocs.io](https://gnlse.readthedocs.io)

## Installation

1. Create a virtual environment with `python -m venv gnlse` or using `conda`.
2. Activate it with `. gnlse/bin/activate`.
3. Clone this repository `git clone https://github.com/WUST-FOG/gnlse-python.git`
4. Install the requirements in this directory `pip install -r requirements.txt`.
5. Install gnlse package `pip install .` (or `pip install -v -e .` for develop mode) or set `PYTHONPATH` enviroment variable

```bash
python -m venv gnlse
. gnlse/bin/activate
git clone https://github.com/WUST-FOG/gnlse-python.git
cd gnlse-python
pip install -r requirements
pip install .
```

## Usage

We provided some examples in `examples` subdirectory. They can be run by typing 
name of the script without any arguments.

Example:

```bash
cd gnlse-python/examples

python test_Dudley.py
```

And you expect to visualise supercontinuum generation process in use of 3 types
 of pulses (simulation similar to Fig.3 of Dudley et. al, RMP 78 1135 (2006)):

![supercontinuum_generation](https://github.com/WUST-FOG/gnlse-python/raw/master/data/supercontinuum_3pulses.png)

### Major features

- **Modular Design**

  Main core of gnlse module is derived from the RK4IP matlab script
  written by J.C.Travers, H. Frosz and J.M. Dudley
  that is provided in "Supercontinuum Generation in Optical Fibers",
  edited by J. M. Dudley and J. R. Taylor (Cambridge 2010).
  The toolbox prepares integration using SCIPYs ode solvers (adaptive step size).
  We decompose the solver framework into different components
  and one can easily construct a customized simulations
  by accounting different physical phenomena, ie. self stepening, Raman response.
  
- **Raman response models**

  We implement three different raman response functions:
    - 'blowwood':   Blow and D. Wood, IEEE J. of Quant. Elec., vol. 25, no. 12, pp. 2665–2673, Dec. 1989,
    - 'linagrawal': Lin and Agrawal, Opt. Lett., vol. 31, no. 21, pp. 3086–3088, Nov. 2006,
    - 'hollenbeck': Hollenbeck and Cantrell, J. Opt. Soc. Am. B, vol. 19, no. 12, Dec. 2002.

- **Nonlinearity**

  We implement the possibility to account effective mode area's dependence on frequency:
    - provide float value for gamma (effective nonlinear coefficient)
    - 'NonlinearityFromEffectiveArea': introduce effective mode area's dependence on frequency (J. Laegsgaard, Opt. Express, vol. 15, no. 24, pp. 16110-16123, Nov. 2007).

- **Dispersion operator**

  We implement two version of dispersion operator:
    - dispersion calculated from Taylor expansion,
    - dispersion calculated from effective refractive indicies.

- **Available demos**

  We prepare few examples in `examples` subdirectory:
    - plot_input_pulse.py: plots envelope of different impulse shapes,
    - plot_Raman_response.py: plots different Raman in temporal domain,
    - test_3rd_order_soliton.py: evolution of the spectral and temporal characteristics of the 3rd order soliton,
    - test_dispersion.py: example of supercontinuum generation using different dispersion operators,
    - test_nonlinearity.py: example of supercontinuum generation using different GNLSE and M-GNLSE (take into account mode profile dispersion),
    - test_Dudley.py: example of supercontinuum generation with three types of input pulse,
    - test_gvd.py: example of impuls broadening due to group velocity dispersion,
    - test_import_export.py: example of saving file with `.mat` extension,
    - test_raman.py: example of soliton fision for diffrent raman response functions,
    - test_spm.py: example of self phase modulation,
    - test_spm+gvd.py: example of generation of 1st order soliton.

## Release History

v1.1.2 was released in 30/8/2021.
The master branch works with **python 3.7**.

* **1.1.2 -> Aug 30th, 2021**
    * ADD: Continious wave envelope
    * FIX: Shift scalling data for nonlinear coefficient
* **1.1.1 -> Aug 28th, 2021**
    * CHANGE: Minor bug fix with scaling
    * CHANGE: Few minor changes in the documentation
* **1.1.0 -> Aug 21st, 2021**
    * Modified-GNLSE extension
    * CHANGE: Code refactor - relocate GNLSE's attribiutes setting into constructor
    * ADD: Possibility to take into account the effective mode area's dependence on frequency
* **1.0.0 -> Aug 13th, 2020**
    * The first proper release
    * CHANGE: Complete documentation and code

## Authors

- [Adam Pawłowski](https://github.com/adampawl)
- [Paweł Redman](https://redman.xyz/)
- [Daniel Szulc](http://szulc.xyz/)
- [Magda Zatorska](https://github.com/magdazatorska)
- [Sylwia Majchrowska](https://majsylw.netlify.app/)
- [Karol Tarnowski](http://www.if.pwr.wroc.pl/~tarnowski/)

## Acknowledgement

*gnlse-python* is an open source project that is contributed by researchers, 
engineers, and students from Wroclaw University of Science and Technology 
as a part of Fiber Optics Group's nonlinear simulations projects. 
The python code based on MATLAB code published in
'Supercontinuum Generation in Optical Fibers'
by J. M. Dudley and J. R. Taylor, available at 
[http://scgbook.info/](http://scgbook.info/).

## Citation

```
@misc{WUST-FOG2020,
  author = {Paw\lowski, A., Redman, P., Szulc, D., Zatorska, M., 
            Majchrowska, S., Tarnowski, K.
           },
  title = {gnlse-python},
  year = {2020},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/WUST-FOG/gnlse-python}},
}
```

## Contributing
Pull requests are welcome. 
For major changes, please open an issue first to discuss 
what you would like to change.

Please make sure to update example tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
