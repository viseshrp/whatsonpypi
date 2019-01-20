# -*- coding: utf-8 -*-

"""Module containing the core functionality."""
from __future__ import unicode_literals  # unicode support for py2

from functools import partial

from .client import WoppClient
from .utils import clean_response


def get_query_response(package=None, more_out=False):
    """
    Run query against PyPI API

    :param package: name of package
    :param more_out: should output should contain more detail?
    :return: output
    """
    client = WoppClient(request_hooks={'response': partial(clean_response, more_out=more_out)})
    response = client.request(package=package)
    out_dict = response.json
    # default out
    return out_dict


if __name__ == '__main__':
    get_query_response('django')
