import os
import sys


sys.path.insert(0, os.path.abspath('..'))

project = 'gnlse-python'
copyright = '2020, Developers of gnlse-python'
author = 'Developers of gnlse-python'

master_doc = 'index'


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'numpydoc',
]

autodoc_mock_imports = [
    'hdf5storage',
    'matplotlib',
    'matplotlib.pyplot',
    'numpy',
    'pyfftw',
    'scipy',
    'scipy.integrate',
    'scipy.interpolate',
    'tqdm',
]

autosummary_generate = True
numpydoc_show_class_members = False

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
