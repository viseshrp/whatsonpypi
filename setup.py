"""The setup script."""
import os

from setuptools import find_packages, setup

REQUIREMENTS = ["click>=8.1.0", "requests>=2.28.0"]

curr_dir = os.path.abspath(os.path.dirname(__file__))


def get_file_text(file_name):
    with open(os.path.join(curr_dir, file_name), encoding="utf-8") as in_file:
        return in_file.read()


_init = {}
_init_file = os.path.join(curr_dir, "whatsonpypi", "__init__.py")
with open(_init_file) as fp:
    exec(fp.read(), _init)
name = _init["__name__"]
author = _init["__author__"]
email = _init["__email__"]
version = _init["__version__"]

setup(
    name=name,
    version=version,
    description="CLI tool to get package info from PyPI and add to requirements.",
    long_description=get_file_text("README.md") + "\n\n" + get_file_text("CHANGELOG.md"),
    long_description_content_type="text/markdown",
    author=author,
    author_email=email,
    maintainer=author,
    maintainer_email=email,
    license="MIT license",
    packages=find_packages(include=["whatsonpypi"], exclude=["tests", "tests.*"]),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    url="https://github.com/viseshrp/whatsonpypi",
    project_urls={
        "Documentation": "https://github.com/viseshrp/whatsonpypi#readme",
        "Changelog": "https://github.com/viseshrp/whatsonpypi/blob/develop/CHANGELOG.md",
        "Bug Tracker": "https://github.com/viseshrp/whatsonpypi/issues",
        "Source Code": "https://github.com/viseshrp/whatsonpypi",
        "CI": "https://github.com/viseshrp/whatsonpypi/actions",
    },
    python_requires=">=3.7",
    keywords="whatsonpypi wopp pypi requirements virtualenv venv",
    test_suite="tests",
    tests_require=[
        "pytest",
    ],
    install_requires=REQUIREMENTS,
    entry_points={
        "console_scripts": [
            "whatsonpypi=whatsonpypi.__main__:main",
        ],
    },
)
