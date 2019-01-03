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


class PackageAbsentException(WoppException):
    """
    Raised when no package is available for the client to request
    """
