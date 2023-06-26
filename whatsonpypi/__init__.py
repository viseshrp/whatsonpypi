"""Top-level package for whatsonpypi."""

__author__ = """Visesh Prasad"""
__email__ = "viseshrprasad@gmail.com"
__name__ = "whatsonpypi"

try:
    from ._version import __version__
except ImportError:  # pragma: no cover
    __version__ = "0.3.7"
