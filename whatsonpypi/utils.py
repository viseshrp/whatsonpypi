from __future__ import annotations

import re
from typing import Any

import click

try:
    from rich import box
    from rich.console import Console
    from rich.table import Table

    _HAS_RICH = True
except ImportError:
    _HAS_RICH = False

from .constants import REQ_LINE_REGEX


def parse_pkg_string(in_str: str) -> tuple[str | None, str | None, str | None]:
    """
    Extract package name and pinned version from a string using the '==' specifier.

    Only supports 'package==version' format. If no version is given, returns the package name alone.

    :param in_str: Raw input string (e.g. 'requests==2.31.0' or 'requests')
    :return: A tuple of (package name, version, specifier), or (name, None, None) if not matched
    """
    match = re.match(REQ_LINE_REGEX, in_str.strip())
    if match:
        groups = match.groupdict()
        return groups["package"], groups["version"], "=="
    return in_str.strip(), None, None


def pretty(data: dict[str, Any], indent: int = 0) -> None:
    """
    Pretty print dictionary output.

    If `rich` is installed, renders a stylized table.
    Otherwise falls back to plain click-based indentation output.

    :param data: Dictionary to print
    :param indent: Indentation level (used only in fallback mode)
    """
    if _HAS_RICH:
        console = Console()
        table = Table(
            title="📦 PyPI Package Info",
            title_style="bold yellow",
            show_header=False,
            show_lines=True,
            box=box.ROUNDED,
            padding=(0, 1),
        )

        # Define columns without headers (no name arguments here!)
        table.add_column(justify="right", style="bold magenta", no_wrap=True, width=26)
        table.add_column(style="white", overflow="fold")

        for key, value in data.items():
            if isinstance(value, dict):
                value = "\n".join(f"{k}: {v}" for k, v in value.items())
            elif isinstance(value, list):
                value = ", ".join(str(v) for v in value)
            table.add_row(key.replace("_", " ").title(), str(value))

        console.print(table)
    else:
        def format_key(key_: str) -> str:
            return key_.upper().replace("_", " ")

        for key, value in data.items():
            if value:
                click.secho("\t" * indent + format_key(key), fg="green", bold=True)
                if isinstance(value, dict):
                    pretty(value, indent + 1)
                else:
                    click.echo("\t" * (indent + 1) + str(value))


def clean_response(r: Any, *_args: Any, **_kwargs: Any) -> Any:
    """
    Hook called after a response is received.
    Used to modify response.

    :param r: requests.models.Response object
    :return: modified Response object
    """
    if r.status_code != 200:
        return r

    def convert_pkg_info(pkg_url_list: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
        """
        Converts a list of package info dicts into a dict keyed by packagetype.
        """
        result: dict[str, dict[str, Any]] = {}
        for pkg in pkg_url_list:
            key = pkg.get("packagetype")
            if key:
                digests = pkg.get("digests") or {}
                result[key] = {
                    "md5": digests.get("md5"),
                    "sha256": digests.get("sha256"),
                    "filename": pkg.get("filename"),
                    "size": pkg.get("size"),
                    "upload_time": pkg.get("upload_time"),
                    "url": pkg.get("url"),
                }
        return result

    dirty = r.json()
    clean: dict[str, Any] = {}

    info = dirty.get("info")
    if info:
        clean = {
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

    releases = dirty.get("releases")
    if releases:
        release_list = list(releases.keys())[::-1]
        releases_info = {
            version: convert_pkg_info(files)
            for version, files in releases.items()
            if files
        }
        clean.update({
            "releases": release_list,
            "releases_pkg_info": releases_info,
        })

    urls = dirty.get("urls")
    if urls:
        clean["latest_pkg_urls"] = convert_pkg_info(urls)

    r.cleaned_json = clean  # type: ignore[attr-defined]
    return r
