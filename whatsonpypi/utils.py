import re

import click

from .constants import REQ_LINE_REGEX


def parse_pkg_string(in_str):
    """
    Use regex to extract package and version

    :param in_str: input string
    :return: tuple of pkg, version
    """
    package = None
    version = None
    spec = None

    try:
        reg_search = re.search(REQ_LINE_REGEX, in_str)
        if reg_search:
            package = reg_search.group(1)
            spec = reg_search.group(2)
            version = reg_search.group(7)
    except IndexError:
        pass

    return package, version, spec


def pretty(input_, indent=0):
    """
    Pretty print dictionary

    :param input_: input
    :param indent: number of tabs
    :return: None
    """

    def get_readable_key(key_):
        # capitalize and remove _
        if "_" in key_:
            return key_.upper().replace("_", " ")
        else:
            return key_.upper()

    if isinstance(input_, dict):
        for key, value in input_.items():
            # only print if there's something
            if value:
                click.secho(
                    "\t" * indent + get_readable_key(str(key)), fg="green", bold=True
                )
                if isinstance(value, dict):
                    pretty(value, indent + 1)
                else:
                    click.echo("\t" * (indent + 1) + str(value))
    else:
        click.echo(input_)


def clean_response(r, *args, **kwargs):
    """
    Hook called after a response is received.
    Used to modify response.

    :param r: requests.models.Response object
    :param args:
    :param kwargs:
    :return: modified Response object
    """

    def convert_pkg_info(pkg_url_list):
        """
        Converts a list of package info dicts
        into a dict, where the key is the type
        of package.. eg: sdist
        :param pkg_url_list:
        :return: dict
        """
        package_urls = {}
        for pkg_url in pkg_url_list:
            package_urls.update(
                {
                    pkg_url.get("packagetype"): {
                        "md5": pkg_url.get("digests").get("md5"),
                        "sha256": pkg_url.get("digests").get("sha256"),
                        "filename": pkg_url.get("filename"),
                        "has_sig": pkg_url.get("has_sig"),
                        "size": pkg_url.get("size"),
                        "upload_time": pkg_url.get("upload_time"),
                        "url": pkg_url.get("url"),
                    }
                }
            )
        return package_urls

    # only run hooks for 200
    if r.status_code == 200:
        r.hook_called = True  # flag to confirm hook was called.

        dirty_response = r.json()
        cleaned_response = {}

        info = dirty_response.get("info")
        if info:
            cleaned_response = {
                "name": info.get("name"),
                "latest_version": info.get("version"),
                "summary": info.get("summary"),
                "homepage": info.get("home_page"),
                "package_url": info.get("project_url") or info.get("package_url"),
                "author": info.get("author"),
                "project_urls": info.get("project_urls"),
                "requires_python": info.get("requires_python"),
                "license": info.get("license"),
                "author_email": info.get("author_email"),
                "latest_release_url": info.get("release_url"),
                "dependencies": info.get("requires_dist"),
            }

        # release list
        releases = dirty_response.get("releases")
        if releases:
            release_list = list(releases.keys())
            release_list.reverse()

            # more detailed info of every release's package
            releases_info = {}
            for key, val in releases.items():
                if val:
                    releases_info[key] = convert_pkg_info(val)

            cleaned_response.update(
                {
                    "releases": release_list,
                    "releases_pkg_info": releases_info,
                }
            )

        # latest release's package information
        latest_pkg_urls = dirty_response.get("urls")
        if latest_pkg_urls:
            cleaned_response.update(
                {
                    "latest_pkg_urls": convert_pkg_info(latest_pkg_urls),
                }
            )

        r.cleaned_json = cleaned_response
    return r
