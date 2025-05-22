from __future__ import annotations

from typing import Any

import click

from .client import WoppClient
from .exceptions import (
    DocsNotFoundError,
    PageNotFoundError,
    URLLaunchError,
)
from .utils import clean_response


def get_output(response: Any, more_out: bool = False) -> dict[str, Any]:
    """
    Returns final output to display

    :param response: WoppResponse object to get the info
    :param more_out: more or less information?
    :return: dict containing output information
    """
    out_dict = {
        "name": response.name,
        "current_version": response.latest_version,
        "summary": response.summary,
        "homepage": response.homepage,
        "package_url": response.package_url,
        "author": response.author,
    }

    if more_out:
        out_dict.update(
            {
                "author_email": response.author_email,
                "releases": ", ".join(response.releases),
                "project_urls": response.project_urls,
                "requires_python": response.requires_python,
                "license": response.license,
                "current_release_url": response.latest_release_url,
                "current_package_info": response.latest_pkg_urls,
                "dependencies": ", ".join(response.dependencies),
            }
        )
    else:
        out_dict.update(
            {
                "latest_releases": (
                    ", ".join(response.latest_releases) if response.latest_releases else None
                ),
            }
        )

    return out_dict


def run_query(
    package: str,
    version: str | None,
    more_out: bool,
    launch_docs: bool,
    open_page: bool,
) -> dict[str, Any] | None:
    """
    Run query against PyPI API and then do stuff based on user options.

    :param package: name of package
    :param version: version of package
    :param more_out: should output should contain more detail?
    :param open_page: should the PyPI page be launched?
    :param launch_docs: should doc URL be launched?

    :return: output if available, or None
    """
    package = package.lower()
    client = WoppClient(request_hooks={"response": clean_response})
    response = client.request(package=package, version=version)

    # launch of docs url
    if launch_docs or open_page:
        if launch_docs:
            url = response.project_docs
            if not url:
                raise DocsNotFoundError
        else:
            url = response.package_url
            if not url:
                raise PageNotFoundError

        exit_status = click.launch(url)
        if exit_status:
            raise URLLaunchError

        return None

    # get the output
    out_dict = get_output(response, more_out=more_out)
    # default out
    return out_dict
