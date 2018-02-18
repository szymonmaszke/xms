#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Utilities for database creation, like verbose printing."""

import sys


__all__ = ['print_verbose', 'store_data']

def print_verbose(message: str, verbose: bool):
    """Print message to stderr if verbose flag is set.

    Parameters
    ----------
    message: str
           Message to be printed
    verbose: bool
           Verbosity flag. If true, message will be printed.

    """
    if verbose:
        print(message, file=sys.stderr)


def store_data(data1: str, data2: str, directory: str, file: str):
    """[CONVENIENCE FUNCTION].

    Stores fragile data inside specified directory and encodes them.

    Parameters
    ----------
    data1 : str
           String containing informations
    data2 : str
           String containing informations
    directory : str
           Directory name used for data saving
    file : str
           File name used for data saving

    Returns
    -------
    type
         <return description>

    """
    if not os.path.exists(os.path.expanduser(directory)):
        try:
            os.makedirs(os.path.expanduser(directory))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    with open(os.path.expanduser(directory + file), 'w') as f:
        f.writelines(
            (base64.b64encode(data1.encode('utf-8'))).decode('utf-8') + '\n' +
            (base64.b64encode(data2.encode('utf-8'))).decode('utf-8'))
