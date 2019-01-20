# -*- coding: utf-8 -*-

"""Module containing the core functionality."""
from __future__ import unicode_literals  # unicode support for py2

from .client import WoppClient
from .utils import clean_response


def get_output(response, more_out=False):
    out_dict = {
        'name': response.name,
        'latest_version': response.latest_version,
        'summary': response.summary,
        'homepage': response.homepage,
        'package_url': response.package_url,
        'author': response.author,
    }

    if more_out:
        out_dict.update({
            'author_email': response.author_email,
            'releases': ', '.join(response.releases),
            'project_urls': response.project_urls,
            'requires_python': response.requires_python,
            'license': response.license,
            'latest_release_url': response.latest_release_url,
            'dependencies': response.dependencies,
        })
    else:
        out_dict.update({
            'latest_releases': ', '.join(response.latest_releases),
        })

    return out_dict


def get_query_response(package=None, more_out=False):
    """
    Run query against PyPI API

    :param package: name of package
    :param more_out: should output should contain more detail?
    :return: output
    """
    client = WoppClient(request_hooks={'response': clean_response})
    response = client.request(package=package)
    out_dict = get_output(response, more_out=more_out)
    # default out
    return out_dict


if __name__ == '__main__':
    get_query_response('django')
