# -*- coding: utf-8 -*-

"""Module containing the core functionality."""
from __future__ import unicode_literals  # unicode support for py2

import glob
import re
import collections
import click

from itertools import chain

from .client import WoppClient
from .constants import REQUIREMENTS_FILE_PATTERN, REQUIREMENTS_REPLACE_COMMENT
from .exceptions import (
    DocsNotFoundError,
    URLLaunchError
)
from .utils import clean_response, convert_to_int_list

ALL_OPTION = 'ALL'


def get_output(response, more_out=False):
    """
    Returns final output to display

    :param response: WoppResponse object to get the info
    :param more_out: more or less information?
    :return: dict containing output information
    """
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


def get_req_files(req_dir):
    req_files = glob.glob(req_dir + "/" + REQUIREMENTS_FILE_PATTERN)
    # prompt user only if there's more than one requirements file.
    num_req_files = len(req_files)

    # if there's only one file available, don't prompt.
    if num_req_files > 1:
        file_choice_list = list(chain(req_files, [ALL_OPTION]))
        # add the `all` option

        choice_map = collections.OrderedDict(
            ('{}'.format(i), value) for i, value in enumerate(file_choice_list, 1)
        )  # creates dict of form {'1': './requirements.txt', ...}

        choices = choice_map.keys()
        default_choice = file_choice_list.index(ALL_OPTION) + 1

        # build prompt
        choice_lines = ['{} - {}'.format(k, v) for k, v in choice_map.items()]
        prompt_text = '\n'.join([
            "We found {} files matching the pattern '{}'. Please choose if"
            " you'd like to modify just one, many or all of them. You can specify"
            " one or multiple options with a comma.. example: 1,2,3 or just 4."
            " '{}' means that all files will be checked and modified. Hit Ctrl+C to"
            " quit".format(num_req_files, REQUIREMENTS_FILE_PATTERN, ALL_OPTION),
            '\n'.join(choice_lines),
            "Choose from {}".format(', '.join(choices))
        ])

        # prompt user
        req_file_ids = click.prompt(
            prompt_text,
            type=str,
            show_default=True,
            value_proc=convert_to_int_list,
        )
        # if the all option is not included in the input,
        # only use the files that are needed.
        if default_choice not in req_file_ids:
            try:
                req_files = [choice_map[str(id_)] for id_ in req_file_ids if id_ != default_choice]
            except KeyError:
                raise click.exceptions.UsageError("Sorry, that's not a valid option.")

    return req_files


def add_pkg_to_req(package, version, req_dir):
    req_files = get_req_files(req_dir)

    for file_path in req_files:
        needs_append = True  # should we append package to the end of file

        click.echo("Modifying file {} ...".format(file_path))
        with open(file_path, 'r+') as file:
            # read all lines at once into memory.
            # NOTE: This is not memory efficient, but requirements files are small
            # so this is good for now. Another way would be to create another file
            # and write to it, but that seems overkill for now.
            data = file.readlines()
            for line_num, line in enumerate(data):
                line = line.strip()
                if line:
                    # first, search if the pkg already exists
                    if package.lower() in line.lower():
                        package_, version_ = re.split("==|>=|<=", line)
                        needs_append = False
                        # if yes, check the version.
                        if version != version_:
                            # replace and end it.
                            data[line_num] = line.replace(version_, version + "\n")
                        else:
                            click.echo("Package is already set to the latest/desired version.")
                        break
                    # if pkg is absent, check for the '#wopp' comment.
                    # ignore case, handle empty spaces
                    if REQUIREMENTS_REPLACE_COMMENT.lower() in line.lower().replace(' ', ''):
                        # only replace the first instance of #wopp
                        needs_append = False
                        data[line_num] = line.replace(line, "{}=={}\n".format(package, version))
                        break

            # move pointer back to start
            file.seek(0, 0)
            # write data
            file.writelines(data)
            # truncate rest of the file
            file.truncate()

        if needs_append:
            # if none of the above cases happen,
            # just append to the end of the file and done.
            with open(file_path, 'a') as file:
                file.write("{}=={}\n".format(package, version))


def get_query_response(
    package=None,
    version=None,
    more_out=False,
    launch_docs=False,
    add_to_req=False,
    req_dir=None
):
    """
    Run query against PyPI API and then do stuff based on user options.

    :param package: name of package
    :param version: version of package
    :param more_out: should output should contain more detail?
    :param launch_docs: should doc URL be launched?
    :param add_to_req: should the package be added as a dependency to requirements files?
    :param req_dir: Directory to search for requirement files
    :return: output if available, or None
    """
    client = WoppClient(request_hooks={'response': clean_response})
    response = client.request(package=package, version=version)

    # launch of docs url
    if launch_docs:
        url = response.project_docs
        if not url:
            raise DocsNotFoundError("Could not find any documentation or homepage URL to launch.")

        exit_status = click.launch(url)
        if exit_status:  # if 1
            raise URLLaunchError("There was a problem opening the URL in your browser.")

        return

    # add pkg as dep to requirements files if needed.
    if add_to_req:
        add_pkg_to_req(response.name, version or response.latest_version, req_dir)
        return

    # get the output
    out_dict = get_output(response, more_out=more_out)
    # default out
    return out_dict
