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

No real magic here. It uses the `requests` package to hit the public [PyPI
REST API](https://docs.pypi.org/api/json/), parses the JSON and displays it.
Embarrassingly simple.

## 📐 Requirements

* Python >= 3.9

## 📦 Installation

```bash
pip install whatsonpypi
```

**OR**

```bash
pip install whatsonpypi[rich]
```
... if you want to use the `rich` package for a nicer output.

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

  A CLI tool to get package info from PyPI.

  Example usages:

  $ whatsonpypi django

  OR

  $ wopp django

Options:
  -v, --version          Show the version and exit.
  -m, --more             Flag to enable expanded output
  -d, --docs             Flag to open docs or homepage of project
  -o, --open             Flag to open PyPI page
  -H, --history INTEGER  Show release history. Use positive number for most
                         recent, negative for oldest. E.g. '--history -10' or '
                         --history 10'
  -h, --help             Show this message and exit.

```
<!-- [[[end]]] -->

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

## 🧾 Changelog

See [CHANGELOG.md](https://github.com/viseshrp/whatsonpypi/blob/main/CHANGELOG.md)

## 🙏 Credits

* [Click](https://click.palletsprojects.com), for enabling delightful CLI development.
* Inspired by [Simon Willison](https://github.com/simonw)'s work.

## 📄 License

MIT © [Visesh Prasad](https://github.com/viseshrp)
