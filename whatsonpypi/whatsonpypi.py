# -*- coding: utf-8 -*-

"""Module containing the core functionality."""
from __future__ import unicode_literals  # unicode support for py2

from .client import WoppClient
from .utils import clean_response


def get_query_response(package=None, version=None):
    """
    Run query against PyPI API

    :param package: name of package
    :param version: version of package
    :return:
    """
    client = WoppClient(request_hooks={'response': clean_response})
    response = client.request(package=package, version=version)

    # returns version by default
    return response.latest_version
