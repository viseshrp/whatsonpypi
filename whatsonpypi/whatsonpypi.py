import collections
import glob
import re

import click

from .client import WoppClient
from .constants import (
    REQUIREMENTS_REPLACE_COMMENT,
    REQ_LINE_REGEX,
    ALL_OPTION,
    REQUIREMENTS_SPEC_MAP,
)
from .exceptions import (
    DocsNotFoundError,
    URLLaunchError,
    RequirementsFilesNotFoundError,
)
from .param_types import MultipleChoice
from .utils import clean_response, extract_pkg_version


def get_output(response, more_out=False):
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
                "releases": ", ".join(response.releases) if response.releases else None,
                "project_urls": response.project_urls,
                "requires_python": response.requires_python,
                "license": response.license,
                "current_release_url": response.latest_release_url,
                "current_package_info": response.latest_pkg_urls,
                "dependencies": ", ".join(response.dependencies)
                if response.dependencies
                else None,
            }
        )
    else:
        out_dict.update(
            {
                "latest_releases": ", ".join(response.latest_releases)
                if response.latest_releases
                else None,
            }
        )

    return out_dict


def get_req_files(req_dir, req_pattern):
    """
    Get the list of requirements files in the desired dir.

    :param req_dir: The dir to search for files
    :param req_pattern: The file name pattern to search for.
    :return:
    """
    req_files = glob.glob(req_dir + "/" + req_pattern)
    # prompt user only if there's more than one requirements file.
    num_req_files = len(req_files)

    if not num_req_files:
        raise RequirementsFilesNotFoundError(
            "No files were found matching pattern '{}' in the provided directory path :\n{}".format(
                req_pattern, req_dir
            )
        )

    # if there's only one file available, don't prompt.
    if num_req_files > 1:
        file_choice_list = [ALL_OPTION]
        file_choice_list.extend(req_files)
        # add the `all` option

        choice_map = collections.OrderedDict(
            ("{}".format(i), value) for i, value in enumerate(file_choice_list, 1)
        )  # creates dict of form {'1': './requirements.txt', ...}

        choices = choice_map.keys()
        default_choice = "1"

        # build prompt
        choice_lines = ["{} - {}".format(k, v) for k, v in choice_map.items()]
        prompt_text = "\n".join(
            [
                "We found {} files matching the pattern '{}'. Please choose if"
                " you'd like to modify just one, many or all of them. You can specify"
                " one or multiple options with a comma.. \nExamples:\n1,2,3\n1\n"
                "'{}' means that all files will be checked and modified, which is the"
                " default. Hit Ctrl+C to quit.".format(
                    num_req_files, req_pattern, ALL_OPTION
                ),
                "\n".join(choice_lines),
                "Hit Enter to use the default or choose from the options",
            ]
        )

        # prompt user
        req_file_ids = click.prompt(
            prompt_text,
            type=MultipleChoice(choices),
            default=default_choice,
            show_default=True,
            show_choices=True,
        )
        # if the all option is not included in the input,
        # only use the files that are needed.
        if default_choice not in req_file_ids:
            req_files = [
                choice_map[str(id_)] for id_ in req_file_ids if id_ != default_choice
            ]

    return req_files


def add_pkg_to_req(package, version, spec, req_dir, req_pattern, comment):
    """
    Actual file operations of the req file happen here.

    :param package: queried package
    :param version: desired version
    :param spec: requirements specification
    :param req_dir: dir containing the req files
    :param req_pattern: search pattern for file names
    :param comment: comment to add, if any
    :return:
    """
    req_files = get_req_files(req_dir, req_pattern)
    req_line = "{}{}{}\n".format(package, REQUIREMENTS_SPEC_MAP[spec], version)

    repl_str = ""
    if comment:
        # add comment if provided.
        repl_str += "# {}\n".format(comment)
    repl_str += req_line

    click.echo("Adding {} ...".format(req_line))
    for file_path in req_files:
        needs_append = True  # should we append package to the end of file

        click.echo("Modifying file: {} ...".format(file_path))
        with open(file_path, "r+", encoding="utf-8") as file:
            # read all lines at once into memory.
            # NOTE: This is not memory efficient, but requirements files are small
            # so this is good for now. Another way would be to .readline() in a while loop,
            # modify it if needed, append it to a temporary file, and in the end, copy all
            # the contents over and overwrite the source file, but that seems overkill.
            data = file.readlines()
            for line_num, line in enumerate(data):
                line = line.strip().lower()
                if line:
                    # first, search if the pkg already exists
                    if not line.startswith("#"):  # not a comment
                        # extract the line contents
                        package_, version_ = extract_pkg_version(line)
                        # compare the line contents to the queried package
                        if package.lower() == package_:
                            # we found it somewhere in the file,
                            # so need to append anymore
                            needs_append = False
                            # if yes, check if version exists or is the desired version
                            if not version or version != version_:
                                # replace and end it.
                                data[line_num] = re.sub(REQ_LINE_REGEX, req_line, line)
                            else:
                                click.echo(
                                    "Package is already set to the latest/desired version."
                                )
                            break

                    # if pkg is absent, check for the '#wopp' comment.
                    # handle empty spaces
                    if REQUIREMENTS_REPLACE_COMMENT.lower() in line.replace(" ", ""):
                        needs_append = False

                        data[line_num] = line.replace(line, repl_str)
                        # only replace the first instance of #wopp
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
            with open(file_path, "a", encoding="utf-8") as file:
                file.write("\n{}".format(repl_str))


def run_query(
    package,
    version,
    more_out,
    launch_docs,
    add_to_req,
    req_dir,
    req_pattern,
    comment,
    spec,
):
    """
    Run query against PyPI API and then do stuff based on user options.

    :param package: name of package
    :param version: version of package
    :param more_out: should output should contain more detail?
    :param launch_docs: should doc URL be launched?
    :param add_to_req: should the package be added as a dependency to requirements files?
    :param comment: comment to be added for the dependency
    :param req_dir: Directory to search for requirement files
    :param req_pattern: Filename pattern for searching requirements files
    :param spec: Requirement Specifiers

    :return: output if available, or None
    """
    client = WoppClient(request_hooks={"response": clean_response})
    response = client.request(package=package, version=version)

    # launch of docs url
    if launch_docs:
        url = response.project_docs
        if not url:
            raise DocsNotFoundError(
                "Could not find any documentation or homepage URL to launch."
            )

        exit_status = click.launch(url)
        if exit_status:  # if 1
            raise URLLaunchError("There was a problem opening the URL in your browser.")

        return

    # add pkg as dep to requirements files if needed.
    if add_to_req:
        add_pkg_to_req(
            response.name,
            version or response.latest_version,
            spec,
            req_dir,
            req_pattern,
            comment,
        )
        return

    # get the output
    out_dict = get_output(response, more_out=more_out)
    # default out
    return out_dict
