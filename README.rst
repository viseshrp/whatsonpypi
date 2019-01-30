===========
whatsonpypi
===========


.. image:: https://img.shields.io/pypi/v/whatsonpypi.svg
        :target: https://pypi.python.org/pypi/whatsonpypi

.. image:: https://img.shields.io/travis/viseshrp/whatsonpypi.svg
        :target: https://travis-ci.org/viseshrp/whatsonpypi

.. image:: https://readthedocs.org/projects/whatsonpypi/badge/?version=latest
        :target: https://whatsonpypi.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pepy.tech/badge/whatsonpypi
        :target: https://pepy.tech/project/whatsonpypi
        :alt: Downloads


CLI tool to find package info on PyPI


* GitHub: https://github.com/viseshrp/whatsonpypi
* PyPI: https://pypi.python.org/pypi/whatsonpypi
* Free software: MIT license
* Documentation: https://whatsonpypi.readthedocs.io.


Installation
------------
.. code-block:: bash

    pip install -U whatsonpypi


Requirements
------------

#. Python 2.7+


Features
--------

* Find information on a package on PyPI

    Examples:

    .. code-block:: bash

        $ whatsonpypi django
        NAME
            Django
        LATEST VERSION
            2.1.5
        SUMMARY
            A high-level Python Web framework that encourages rapid development and clean, pragmatic design.
        PACKAGE URL
            https://pypi.org/project/Django/
        AUTHOR
            Django Software Foundation
        LATEST RELEASES
            2.2a1, 2.1rc1, 2.1b1, 2.1a1, 2.1.5


* For more information..

    Examples:

    .. code-block:: bash

        $ whatsonpypi django --more
        ...


* Version specific information..

    Examples:

    .. code-block:: bash

        $ whatsonpypi django==2.1.4 --more
        ...


* Launch documentation URL of project in a browser tab

    Examples:

    .. code-block:: bash

        $ whatsonpypi django --docs


* Add packages to your requirements files.

    Examples:

    .. code-block:: bash

        $ whatsonpypi django --add


    By default, it searches for files with names matching ``requirements*.txt``
    in the current working directory and adds the dependency to the end of the
    file.

    You can change the filename pattern to search for. The pattern may contain simple
    shell-style wildcards.

    .. code-block:: bash

        $ whatsonpypi django --add --req-pattern "*.txt"


    **If there's more than one file**, you will see a prompt allowing you to select the files
    that should be modified.

    If you want the dependency to be added to a specific line,
    mention a comment ``#wopp`` on its own line, which will be replaced with the dependency:

    Example:

    Do this in your requirements.txt:

    .. code-block:: yaml

        # Django
        django==2.1.5
        # testing
        pytest==4.1.1
        #wopp

    Then running this:

    .. code-block:: bash

        $ whatsonpypi pytest-runner --add

    will produce this:

    .. code-block:: yaml

        # Django
        django==2.1.5
        # testing
        pytest==4.1.1
        pytest-runner==4.2


    Existing dependencies will be replaced with newer versions. Dependency version
    by default is the latest unless specified explicitly like:

    .. code-block:: bash

        $ whatsonpypi pytest-runner==4.1 --add


    Optionally, directory to search for requirement files can be specified with ``--req-dir``.
    Both absolute and relative paths are allowed. Must be a directory.

    .. code-block:: bash

        $ whatsonpypi pytest-runner==4.1 --add --req-dir /Users/Me/Documents/GitHub/project/requirements

    Default value (if not provided) is the directory where the command is run (cwd).

    Also, optionally, you can specify comments to add before a dependency.
    Note that the comment will not be added if the dependency already exists in the file.

    For example, running this:

    .. code-block:: bash

        $ whatsonpypi pytest-runner --add --comment 'testing'

    will add this:

    .. code-block:: yaml

        # testing
        pytest-runner==4.2

See all options with:

.. code-block:: bash

    $ whatsonpypi --help

Credits
-------

* Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template for getting me started.


.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

