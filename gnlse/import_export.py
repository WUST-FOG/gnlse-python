"""Import and export \\*.mat files.

This module contains functions that enable to read matlab files (\\*.mat)
in python as dictionary, and to export dictionary to \\*.mat.

"""

import hdf5storage as hdf


def read_mat(filename):
    """Imports \\*.mat file as dictionary.

    Parameters
    ----------
    filename : string
        Name of \\*.mat file ('example.mat').

    Returns
    -------
    mat : dict
        dictionary of variables in imported file
        keys - names of variables
        values - variables' values

    """
    mat = hdf.loadmat(filename, appendmat=True)
    return mat


def write_mat(dictionary, filename):
    """Exports dictionary to \\*.mat file.

    Parameters
    ----------
    dictionary : dict
        A list of variables.
    filename : string
        Name of \\*.mat file ('example.mat').
    """

    hdf.savemat(filename,
                dictionary,
                appendmat=True,
                store_python_metadata=True,
                action_for_matlab_incompatible='ignore')
