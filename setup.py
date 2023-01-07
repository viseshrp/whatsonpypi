"""The setup script."""
import os
from io import open

from setuptools import setup, find_packages

REQUIREMENTS = ["click==8.1.3", "requests==2.28.1"]

curr_dir = os.path.abspath(os.path.dirname(__file__))


def get_file_text(file_name):
    with open(os.path.join(curr_dir, file_name), "r", encoding="utf-8") as in_file:
        return in_file.read()


_version = {}
_version_file = os.path.join(curr_dir, "whatsonpypi", "__init__.py")
with open(_version_file) as fp:
    exec(fp.read(), _version)
version = _version["__version__"]

setup(
    name="whatsonpypi",
    version=version,
    description="CLI tool to get package info from PyPI and add to requirements.",
    long_description=get_file_text("README.rst")
    + "\n\n"
    + get_file_text("CHANGELOG.rst"),
    long_description_content_type="text/x-rst",
    author="Visesh Prasad",
    author_email="visesh@live.com",
    maintainer="Visesh Prasad",
    maintainer_email="visesh@live.com",
    license="MIT license",
    packages=find_packages(include=["whatsonpypi"]),
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
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    url="https://github.com/viseshrp/whatsonpypi",
    project_urls={
        "Documentation": "https://github.com/viseshrp/whatsonpypi",
        "Changelog": "https://github.com/viseshrp/whatsonpypi/blob/main/CHANGELOG.md",
        "Bug Tracker": "https://github.com/viseshrp/whatsonpypi/issues",
        "Source Code": "https://github.com/viseshrp/whatsonpypi",
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
