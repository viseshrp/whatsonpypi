from __future__ import annotations

from typing import Any

import click

from .client import WoppClient, WoppResponse
from .exceptions import (
    DocsNotFoundError,
    PageNotFoundError,
    URLLaunchError,
)
from .utils import clean_response


def get_output(response: WoppResponse, more_out: bool = False) -> dict[str, Any]:
    """
    Returns final output to display.

    :param response: WoppResponse object to get the info
    :param more_out: more or less information?
    :return: dict containing output information
    """
    out_dict: dict[str, Any] = {
        "name": response.name,
        "summary": response.summary,
        "author": response.author,
        "package_url": response.package_url,
        "homepage": response.homepage,
        "current_version": response.latest_version,
        "requires_python": response.requires_python,
    }

    if more_out:
        out_dict.update(
            {
                "dependencies": ", ".join(response.dependencies),
                "project_urls": response.project_urls,
                "license": response.license,
                "current_release_url": response.latest_release_url,
                "current_package_info": response.latest_pkg_urls,
                "releases": ", ".join(response.get_sorted_releases()),
            }
        )
    else:
        out_dict["latest_releases"] = ", ".join(response.get_latest_releases())

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
    :param more_out: should output contain more detail?
    :param open_page: should the PyPI page be launched?
    :param launch_docs: should doc URL be launched?

    :return: output if available, or None
    """
    client = WoppClient(request_hooks={"response": clean_response})
    response = client.request(package=package.lower(), version=version)

    if launch_docs:
        url = response.project_docs
        if not url:
            raise DocsNotFoundError
    elif open_page:
        url = response.package_url
        if not url:
            raise PageNotFoundError
    else:
        return get_output(response, more_out=more_out)

    exit_status = click.launch(url)
    if exit_status:
        raise URLLaunchError

    return None
