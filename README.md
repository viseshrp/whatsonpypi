whatsonpypi
===========

[![image](https://img.shields.io/pypi/v/whatsonpypi.svg)](https://pypi.python.org/pypi/whatsonpypi)
[![Python versions](https://img.shields.io/pypi/pyversions/whatsonpypi.svg?logo=python&logoColor=white)](https://pypi.org/project/whatsonpypi/)
<!--[![Tests status](https://github.com/viseshrp/whatsonpypi/workflows/Test/badge.svg)](https://github.com/viseshrp/whatsonpypi/actions?query=workflow%3ATest)-->
<!--[![Coverage](https://codecov.io/gh/viseshrp/whatsonpypi/branch/develop/graph/badge.svg)](https://codecov.io/gh/viseshrp/whatsonpypi)-->
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/viseshrp/whatsonpypi/blob/develop/LICENSE)
[![Downloads](https://pepy.tech/badge/whatsonpypi)](https://pepy.tech/project/whatsonpypi)

Get package info from PyPI. Modify your requirements files.


Why build this
--------------
I find myself checking the PyPI page very frequently mostly when upgrading dependencies to get the 
latest versions. I'm inherently lazy and did not want to get my ass off my terminal window.


How it works
------------
No real magic here. It uses the `requests` package to hit the public PyPI REST API, parses the JSON 
and displays it. There's also some basic file manipulation to modify requirements files. Embarrassingly 
simple.


Installation
------------

``` {.bash}
pip install whatsonpypi
```

Requirements
------------

- Python 3.7+

Features
--------

-   Find information on a package on PyPI

    > Examples:
    >
    > ``` bash
    > $ whatsonpypi django
    > NAME
    >     Django
    > LATEST VERSION
    >     2.1.5
    > SUMMARY
    >     A high-level Python Web framework that encourages rapid development and clean, pragmatic design.
    > PACKAGE URL
    >     https://pypi.org/project/Django/
    > AUTHOR
    >     Django Software Foundation
    > LATEST RELEASES
    >     2.2a1, 2.1rc1, 2.1b1, 2.1a1, 2.1.5
    > ```

-   For more information..

    > Examples:
    >
    > ``` bash
    > $ whatsonpypi django --more
    > ...
    > ```

-   Version specific information..

    > Examples:
    >
    > ``` bash
    > $ whatsonpypi django==2.1.4 --more
    > ...
    > ```

-   Launch PyPI URL of project in a browser tab

    > Examples:
    >
    > ``` bash
    > $ whatsonpypi django --open
    > ```

-   Launch documentation URL of project in a browser tab

    > Examples:
    >
    > ``` bash
    > $ whatsonpypi django --docs
    > ```

-   Add packages to your requirements files.

    > Examples:
    >
    > ``` bash
    > $ whatsonpypi django --add
    > ```
    >
    > By default, it searches for files with names matching
    > `requirements*.txt` in the current working directory and adds the
    > dependency to the end of the file.
    >
    > You can change the filename pattern to search for. The pattern may
    > contain simple shell-style wildcards.
    >
    > ``` bash
    > $ whatsonpypi django --add --req-pattern "*.txt"
    > ```
    >
    > **If there\'s more than one file**, you will see a prompt allowing
    > you to select the files that should be modified.
    >
    > If you want the dependency to be added to a specific line, mention
    > a comment `#wopp` on its own line, which will be replaced with the
    > dependency:
    >
    > Example:
    >
    > Do this in your requirements.txt:
    >
    > ``` yaml
    > # Django
    > django==2.1.5
    > # testing
    > pytest==4.1.1
    > #wopp
    > ```
    >
    > Then running this:
    >
    > ``` bash
    > $ whatsonpypi pytest-runner --add
    > ```
    >
    > will produce this:
    >
    > ``` yaml
    > # Django
    > django==2.1.5
    > # testing
    > pytest==4.1.1
    > pytest-runner==4.2
    > ```
    >
    > Use requirements specifications as needed. `==`, `>=`, `<=` or
    > `~=` using `--ee`, `--ge`, `--le` or `--te`. Default is `--ee`:
    >
    > ``` bash
    > $ whatsonpypi pytest-runner --add --ge
    > ```
    >
    > will produce this:
    >
    > ``` yaml
    > # Django
    > django==2.1.5
    > # testing
    > pytest==4.1.1
    > pytest-runner>=4.2
    > ```
    >
    > Existing dependencies will be replaced with newer versions.
    > Dependency version by default is the latest unless specified
    > explicitly like:
    >
    > ``` bash
    > $ whatsonpypi pytest-runner==4.1 --add
    > ```
    >
    > Note that you may have you to double quote it in order to prevent
    > Bash from parsing it.
    >
    > ``` bash
    > $ whatsonpypi "pytest-runner>=4.1" --add
    > ```
    >
    > Optionally, directory to search for requirement files can be
    > specified with `--req-dir`. Both absolute and relative paths are
    > allowed. Must be a directory.
    >
    > ``` bash
    > $ whatsonpypi pytest-runner==4.1 --add --req-dir /Users/Me/Documents/GitHub/project/requirements
    > ```
    >
    > Default value (if not provided) is the directory where the command
    > is run (cwd).
    >
    > Also, optionally, you can specify comments to add before a
    > dependency. Note that the comment will not be added if the
    > dependency already exists in the file.
    >
    > For example, running this:
    >
    > ``` bash
    > $ whatsonpypi pytest-runner --add --comment 'testing'
    > ```
    >
    > will add this:
    >
    > ``` yaml
    > # testing
    > pytest-runner==4.2
    > ```

Usage
-----

<!-- [[[cog
import cog
from whatsonpypi import cli
from click.testing import CliRunner
runner = CliRunner()
result = runner.invoke(cli.main, ["--help"])
out = result.output.replace("Usage: main", "Usage: whatsonpypi")
cog.out(
    "``` {{.bash}}\n"
    "$ whatsonpypi --help\n"
    "{}\n"
    "```".format(out)
)
]]] -->
``` {.bash}
$ whatsonpypi --help
Usage: whatsonpypi [OPTIONS] PACKAGE

  CLI tool to get package info from PyPI and/or manipulate requirements.

  Example usages:

  $ whatsonpypi django

Options:
  -v, --version            Show the version and exit.
  -m, --more               Flag to enable expanded output  [required]
  -d, --docs               Flag to open docs or homepage of project
  -o, --open               Flag to open PyPI page
  -a, --add                Flag to enable adding of dependencies to requirement
                           files. By default, it searches for files with names
                           matching requirements*.txt in the current working
                           directory and adds the dependency to the end of the
                           file. If you want the dependency to be added to a
                           specific line, mention the comment '#wopp' on its own
                           line which will be replaced with the dependency.
                           Existing dependencies will be replaced with newer
                           versions. Dependency version by default is the latest
                           unless specified explicitly with 'whatsonpypi
                           package==version'. Directory to search for
                           requirement files can be specified with --req-dir
  -r, --req-dir DIRECTORY  Directory to search for requirement files. Only used
                           when --add is used.  [default: .]
  -p, --req-pattern TEXT   Filename pattern for searching requirements files.
                           [default: requirements*.txt; required]
  -c, --comment TEXT       Comment to be added for the dependency when using
                           --add.
  --ee                     use == when adding to requirements.
  --le                     use <= when adding to requirements.
  --ge                     use >= when adding to requirements.
  --te                     use ~= when adding to requirements.
  -h, --help               Show this message and exit.

```
<!-- [[[end]]] -->

Credits
-------

- [Click](https://click.palletsprojects.com), for making writing CLI
    tools a complete pleasure.
- [Simon Willison](https://github.com/simonw/sqlite-utils/) for some
    inspiration.
