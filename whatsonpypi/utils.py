# -*- coding: utf-8 -*-

"""Utility methods"""
from __future__ import unicode_literals  # unicode support for py2


def clean_response(r, *args, **kwargs):
    """
    Hook called after a response is received.
    Used to modify response.

    :param r: requests.models.Response object
    :param args:
    :param kwargs:
    :return: modified Response object
    """
    r.hook_called = True  # placeholder
    return r
