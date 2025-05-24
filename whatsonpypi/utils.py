from __future__ import annotations

from datetime import datetime
import re
from typing import Any

import click

try:
    from rich import box
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table

    _HAS_RICH: bool = True
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


def format_key(key_: str) -> str:
    return key_.upper().replace("_", " ")


def pretty(data: dict[str, Any], indent: int = 0) -> None:
    """
    Pretty print dictionary output.

    If `rich` is installed, renders a stylized table.
    Otherwise falls back to plain click-based indentation output.

    :param data: Dictionary to print
    :param indent: Indentation level (used only in fallback mode)
    """

    def format_value(val: Any) -> str:
        if isinstance(val, str):
            try:
                dt = datetime.fromisoformat(val.replace("Z", "+00:00"))
                return dt.strftime("%b %d, %Y %H:%M")
            except ValueError:
                return val
        return str(val)

    if _HAS_RICH:

        def render_table(input_dict: dict[str, Any]) -> Table:
            table = Table(
                show_header=False,
                show_lines=True,
                box=box.ROUNDED,
                padding=(0, 1),
            )
            table.add_column(justify="right", style="bold magenta", width=26, no_wrap=True)
            table.add_column(style="white", overflow="fold")

            for key, value in input_dict.items():
                if value is None or value == "":
                    continue
                key_label = format_key(str(key))
                if isinstance(value, dict):
                    nested_table = render_table(value)
                    table.add_row(key_label, nested_table)
                elif isinstance(value, list):
                    nested = "\n".join(format_value(item) for item in value)
                    table.add_row(key_label, nested)
                else:
                    table.add_row(key_label, format_value(value))
            return table

        console = Console()
        main_table = render_table(data)
        console.print(
            Panel(
                main_table,
                title="📦 PyPI Package Info",
                title_align="left",
                border_style="yellow",
            )
        )
    else:
        if indent == 0:
            click.secho("📦 PyPI Package Info\n", fg="yellow", bold=True)

        for key, value in data.items():
            if not value:
                continue

            click.secho("\t" * indent + format_key(key), fg="green", bold=True)

            if isinstance(value, dict):
                pretty(value, indent + 1)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        pretty(item, indent + 2)
                    else:
                        click.echo("\t" * (indent + 2) + format_value(item))
            else:
                click.echo("\t" * (indent + 1) + format_value(value))


def filter_info(pkg_url_list: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """
    Converts a list of package info dicts into a dict keyed by packagetype.
    """
    result = {}
    for pkg in pkg_url_list:
        key = pkg.get("packagetype")
        if key:
            digests = pkg.get("digests") or {}
            result[key] = {
                "filename": pkg.get("filename"),
                "size": pkg.get("size"),
                "upload_time": pkg.get("upload_time_iso_8601"),
                "requires_python": pkg.get("requires_python"),
                "python_version": pkg.get("python_version"),
                "url": pkg.get("url"),
                "yanked": pkg.get("yanked"),
                "yanked_reason": pkg.get("yanked_reason"),
                "md5": digests.get("md5"),
                "sha256": digests.get("sha256"),
            }
    return result


def clean_response(r: Any, *_args: Any, **_kwargs: Any) -> Any:
    """
    Hook called after a response is received.
    Used to modify response.

    :param r: requests.models.Response object
    :return: modified Response object
    """
    if r.status_code != 200:
        return r

    dirty = r.json()
    clean = {}

    info = dirty.get("info")
    if info:
        clean = {
            "name": info.get("name"),
            "latest_version": info.get("version"),
            "summary": info.get("summary"),
            "homepage": info.get("home_page"),
            "package_url": info.get("project_url") or info.get("package_url"),
            "author": info.get("author") or info.get("author_email"),
            "project_urls": info.get("project_urls"),
            "requires_python": info.get("requires_python"),
            "license": info.get("license"),
            "latest_release_url": info.get("release_url"),
            "dependencies": info.get("requires_dist"),
        }

    releases = dirty.get("releases")
    if releases:
        release_list = list(releases.keys())
        release_info = {version: filter_info(files) for version, files in releases.items() if files}
        clean.update(
            {
                "releases": release_list,
                "release_info": release_info,
            }
        )

    urls = dirty.get("urls")
    if urls:
        clean["latest_pkg_urls"] = filter_info(urls)

    r.cleaned_json = clean
    return r
