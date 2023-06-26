"""
whatsonpypi.exceptions
-----------------------
All exceptions used in the whatsonpypi code base are defined here.
"""


class WoppError(Exception):
    """
    Base exception. All other exceptions
    inherit from here.
    """


class PackageNotProvidedError(WoppError):
    """
    Raised when no package is available for the client to request
    """


class PackageNotFoundError(WoppError):
    """
    Raised when a package is not found on PyPI
    """


class DocsNotFoundError(WoppError):
    """
    Raised when a package does not have documentation or homepage urls
    """


class URLLaunchError(WoppError):
    """
    Raised when there's a problem opening a URL in the browser
    """


class RequirementsFilesNotFoundError(WoppError):
    """
    Raised when no requirements files are found in provided directory path.
    """
