# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

-

### Fixed

-

### Changed

-

### Removed

-

## [0.4.1] - 2025-05-23

### Fixed

- Fixed CLI help text.

## [0.4.0] - 2025-05-23

### Added

- Added --history/-H flag to show package history.
- Added `rich` support for better output formatting.
  - Use `pip install whatsonpypi[rich]` to enable, OR,
  - Make sure rich is installed in your environment.
- Added a new shorter alias: `wopp`. You can now run `$ wopp requests` instead of `$ whatsonpypi requests`.

### Fixed

- Fixed display of release information.
- List dependencies as a proper list.
- Improved output formatting.
- Fixed browser launching on Windows.

### Changed

- Removed deprecated info from output.
- Modernized codebase structure and tooling.

### Removed

- **BREAKING**: Removed support for adding packages to requirements files.
- **BREAKING**: Dropped Python 3.7 and 3.8 support.
- **BREAKING**: Renamed `--page` to `--open` for opening the PyPI page.
- **BREAKING**: Version specific querying only supports `==` now.

## [0.3.7] - 2023-01-11

### Added

- Added `-o/--page` flag to open PyPI page.

## [0.3.6] - 2023-01-11

### Fixed

- Fixed handling of `None` values from the PyPI API.

## [0.3.5] - 2023-01-10

### Removed

- Removed debug logs.

## [0.3.4] - 2023-01-09

### Fixed

- Fixed null pointer errors.

## [0.3.3] - 2023-01-08

### Changed

- Made version specifications more flexible.

## [0.3.2] - 2023-01-07

### Fixed

- Fixed version and spec parsing logic.

## [0.3.1] - 2023-01-07

### Added

- Added `--le`, `--ge`, `--ee`, and `--te` flags for version specifiers.

## [0.3.0] - 2023-01-06

### Removed

- Dropped Python 2 support. Requires Python 3.7+ now.

## [0.2.8] - 2019-02-13

### Fixed

- More Python 2 compatibility fixes.
- Ensure UTF-8 encoding when opening files.

## [0.2.7] - 2019-02-12

### Fixed

- Fix for `ImportError` on Python 2.

## [0.2.6] - 2019-02-06

### Fixed

- Fixed missing newline characters.

## [0.2.5] - 2019-02-05

### Fixed

- Fixed requirements file format validation.

## [0.2.4] - 2019-01-29

### Added

- Added `--comment` to allow inserting comments alongside `--add`.

## [0.2.3] - 2019-01-26

### Added

- Added `--req-pattern` to allow specifying the filename pattern for requirements files.

### Fixed

- Raise error when no matching requirements files are found.

## [0.2.2] - 2019-01-23

### Fixed

- Fixed display of empty dependencies.

## [0.2.1] - 2019-01-23

### Fixed

- Miscellaneous small fixes.

## [0.2.0] - 2019-01-22

### Added

- Added `-a/--add` to enable writing packages to requirement files.
- Added `-d/--docs` to launch documentation/homepage URLs.
- Support version-specific queries.

## [0.1.2] - 2019-01-20

### Added

- Added `--more` / `-m` flag for detailed package output.
- Displayed more metadata fields in default output.

## [0.1.1] - 2019-01-02

### Added

- First release on PyPI.
