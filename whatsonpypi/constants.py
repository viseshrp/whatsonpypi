"""
Package level constants
"""
PYPI_BASE_URL = "https://pypi.org/pypi"
REQUIREMENTS_REPLACE_COMMENT = "#wopp"
ALL_OPTION = "ALL"
REQ_LINE_REGEX = "([A-Za-z0-9-_.]+)((==)|(~=)|(>=)|(<=))([A-Za-z0-9-_.]+)"
REQUIREMENTS_SPEC_MAP = {
    "ee": "==",
    "le": "<=",
    "ge": ">=",
    "te": "~=",
}
