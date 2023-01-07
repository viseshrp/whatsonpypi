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


class DocsNotFoundError(WoppException):
    """
    Raised when a package does not have documentation or homepage urls
    """


class URLLaunchError(WoppException):
    """
    Raised when there's a problem opening a URL in the browser
    """


class RequirementsFilesNotFoundError(WoppException):
    """
    Raised when no requirements files are found in provided directory path.
    """
