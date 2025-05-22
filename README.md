# whatsonpypi

[![PyPI version](https://img.shields.io/pypi/v/whatsonpypi.svg)](https://pypi.org/project/whatsonpypi/)
[![Python versions](https://img.shields.io/pypi/pyversions/whatsonpypi.svg?logo=python&logoColor=white)](https://pypi.org/project/whatsonpypi/)
[![CI](https://github.com/viseshrp/whatsonpypi/actions/workflows/main.yml/badge.svg)](https://github.com/viseshrp/whatsonpypi/actions/workflows/main.yml)
[![Coverage](https://codecov.io/gh/viseshrp/whatsonpypi/branch/main/graph/badge.svg)](https://codecov.io/gh/viseshrp/whatsonpypi)
[![License: MIT](https://img.shields.io/github/license/viseshrp/whatsonpypi)](https://github.com/viseshrp/whatsonpypi/blob/main/LICENSE)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/en/stable/)
[![Lint: Ruff](https://img.shields.io/badge/lint-ruff-000000.svg)](https://docs.astral.sh/ruff/)
[![Typing: mypy](https://img.shields.io/badge/typing-checked-blue.svg)](https://mypy.readthedocs.io/en/stable/)

> Get package info from PyPI.

![Demo](https://raw.githubusercontent.com/viseshrp/whatsonpypi/main/demo.gif)

## 🚀 Why this project exists

I find myself checking the PyPI page very frequently mostly when upgrading
dependencies to get the latest versions. I'm inherently lazy and did not want
to get my ass off my terminal window.

## 🧠 How this project works

No real magic here. It uses the `requests` package to hit the public PyPI
REST API, parses the JSON and displays it. There's also some basic file
manipulation to modify requirements files. Embarrassingly simple.

## 🛠️ Features

- Find information on a package on PyPI

    > Examples:
    >
    > ``` bash
    > $ whatsonpypi django
    > NAME
    >     Django
    > LATEST VERSION
    >     2.1.5
    > SUMMARY
    >     A high-level Python Web framework that encourages
    > rapid development and clean, pragmatic design.
    > PACKAGE URL
    >     https://pypi.org/project/Django/
    > AUTHOR
    >     Django Software Foundation
    > LATEST RELEASES
    >     2.2a1, 2.1rc1, 2.1b1, 2.1a1, 2.1.5
    > ```

- For more information..

    > Examples:
    >
    > ``` bash
    > $ whatsonpypi django --more
    > ...
    > ```

- Version specific information..

    > Examples:
    >
    > ``` bash
    > $ whatsonpypi django==2.1.4 --more
    > ...
    > ```

- Launch PyPI URL of project in a browser tab

    > Examples:
    >
    > ``` bash
    > $ whatsonpypi django --open
    > ```

- Launch documentation URL of project in a browser tab

    > Examples:
    >
    > ``` bash
    > $ whatsonpypi django --docs
    > ```

## 📦 Installation

```bash
pip install whatsonpypi
```

## 🧪 Usage

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

## 📐 Requirements

* Python >= 3.9

## 🧾 Changelog

See [CHANGELOG.md](https://github.com/viseshrp/whatsonpypi/blob/main/CHANGELOG.md)

## 🙏 Credits

* [Click](https://click.palletsprojects.com), for enabling delightful CLI development.
* Inspired by [Simon Willison](https://github.com/simonw)'s work.

## 📄 License

MIT © [Visesh Prasad](https://github.com/viseshrp)
