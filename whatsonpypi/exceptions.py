# -*- coding: utf-8 -*-

"""
whatsonpypi.exceptions
-----------------------
All exceptions used in the whatsonpypi code base are defined here.
"""


class WoppException(Exception):
    """
    Base exception. All other exceptions
    inherit from here.
    """


class PackageNotProvidedError(WoppException):
    """
    Raised when no package is available for the client to request
    """


class PackageNotFoundError(WoppException):
    """
    Raised when a package is not found on PyPI
    """
