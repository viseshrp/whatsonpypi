"""
whatsonpypi.exceptions
-----------------------
All exceptions used in the code base are defined here.
"""

from __future__ import annotations


class WoppError(Exception):
    """
    Base exception. All other exceptions inherit from here.
    """

    detail: str = "An unexpected error occurred."

    def __init__(self, extra_detail: str | None = None) -> None:
        super().__init__()
        self.extra_detail: str | None = extra_detail

    def __str__(self) -> str:
        if self.extra_detail:
            return f"{self.detail} :: {self.extra_detail}"
        return self.detail


class PackageNotProvidedError(WoppError):
    """Raised when no package is available for the client to request."""

    detail: str = "A package name is needed to proceed."


class PackageNotFoundError(WoppError):
    """Raised when a package is not found on PyPI."""

    detail: str = "Sorry, but that package/version couldn't be found on PyPI."


class DocsNotFoundError(WoppError):
    """Raised when a package does not have documentation or homepage URLs."""

    detail: str = "Could not find any documentation or homepage URL to launch."


class PageNotFoundError(WoppError):
    """Raised when a package does not have the PyPI URL info."""

    detail: str = "Could not find the URL to launch."


class URLLaunchError(WoppError):
    """Raised when there's a problem opening a URL in the browser."""

    detail: str = "There was a problem opening the URL in your browser."
