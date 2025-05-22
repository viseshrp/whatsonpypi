"""
Package level constants
"""

from typing import Final

PYPI_BASE_URL: Final[str] = "https://pypi.org/pypi"
REQUIREMENTS_REPLACE_COMMENT: Final[str] = "#wopp"
ALL_OPTION: Final[str] = "ALL"
REQ_LINE_REGEX: Final[str] = r"([A-Za-z0-9\[\]\-\_\.]+)((==)|(~=)|(>=)|(<=))([A-Za-z0-9\-\_\.]+)"
