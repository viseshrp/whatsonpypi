# -*- coding: utf-8 -*-

"""Module containing the core functionality."""
from __future__ import unicode_literals  # unicode support for py2

import click

from .client import WoppClient
from .exceptions import (
    DocsNotFoundError,
    URLLaunchError
)
from .utils import clean_response


def get_output(response, more_out=False):
    out_dict = {
        'name': response.name,
        'current_version': response.latest_version,
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
            'current_release_url': response.latest_release_url,
            'current_package_info': response.latest_pkg_urls,
            'dependencies': ', '.join(response.dependencies),
        })
    else:
        out_dict.update({
            'latest_releases': ', '.join(response.latest_releases),
        })

    return out_dict


def get_query_response(package=None, version=None, more_out=False, launch_docs=False):
    """
    Run query against PyPI API

    :param package: name of package
    :param version: version of package
    :param more_out: should output should contain more detail?
    :param launch_docs: should doc URL be launched?
    :return: output if available, or None
    """
    client = WoppClient(request_hooks={'response': clean_response})
    response = client.request(package=package, version=version)

    if launch_docs:
        url = response.project_docs
        if not url:
            raise DocsNotFoundError("Could not find any documentation or homepage URL to launch.")

        exit_status = click.launch(url)
        if exit_status:  # if 1
            raise URLLaunchError("There was a problem opening the URL in your browser.")
        
        return

    out_dict = get_output(response, more_out=more_out)
    # default out
    return out_dict


if __name__ == '__main__':
    get_query_response('django')
