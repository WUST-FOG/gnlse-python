import os
import sys


sys.path.insert(0, os.path.abspath('..'))

project = 'gnlse-python'
copyright = '2020, Developers of gnlse-python'
author = 'Developers of gnlse-python'

master_doc = 'index'

extensions = [
    'numpydoc',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary'
]

autodoc_mock_imports = [
    'numpy', 'matplotlib', 'matplotlib.pyplot', 'scipy', 'scipy.integrate',
    'scipy.interpolate', 'pyfftw', 'hdf5storage', 'tqdm'
]

autosummary_generate = True
numpydoc_show_class_members = False

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
html_theme = 'alabaster'
html_static_path = ['_static']
