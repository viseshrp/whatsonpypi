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


* Launch documentation URL of project in a browser tab

    Examples:

    .. code-block:: bash

        $ whatsonpypi django --docs


* More to come ..

See all options with:

.. code-block:: bash

    $ whatsonpypi --help

Credits
-------

* Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template for getting me started.


.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

