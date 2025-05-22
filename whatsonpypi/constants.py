"""
Package level constants
"""

from typing import Final

PYPI_BASE_URL: Final[str] = "https://pypi.org/pypi"
REQ_LINE_REGEX: Final[str] = r"^(?P<package>[A-Za-z0-9_\-\.]+)==(?P<version>[A-Za-z0-9_\.\-]+)$"
