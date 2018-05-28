#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""General utilities (like verbose output decroator)."""

import base64
import os
import sys

from termcolor import colored


def verbose(in_progress: str, success: str):
    """Print message to stdout/stderr using decorator syntax.

    Parameters
    ----------
    in_progress: str
            String displayed if task is in progress
    success: str
            String displayed if task finishes successfully

    Returns
    -------
    Output of decorated function OR exits with error code 1 if any error
    occured.

    """

    def decorator(function):

        def wrapper(*args, **kwargs):
            try:
                print_color(in_progress, "magenta")
                return_values = function(*args, **kwargs)
                print_color(success, "green")
                return return_values
            except VerboseError as error:
                print_color_error(error)
                sys.exit(1)
            except Exception as error:
                print_color_error("Fatal exception, raising error!")
                raise

        return wrapper

    return decorator


def print_color_error(message: str, verbose: bool = True):
    """Print error message to stderr colored red.

    Parameters
    ----------
    message: str
           Message to be printed
    verbose: bool
           Verbosity flag
    """
    print(colored(message, "red", attrs=["bold"]), file=sys.stderr)


def print_color(message: str, color: str, verbose: bool = True):
    """Print message in bold with specified color.

    Parameters
    ----------
    message: str
           Message to be printed
    color: str
           Name of the color (see termcolor for available options)
    verbose: bool
           Verbosity flag
    """
    if verbose:
        print(colored(message, color, attrs=["bold"]))
