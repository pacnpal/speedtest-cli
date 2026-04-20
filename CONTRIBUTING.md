# Contributing to speedtest-cli

Thanks for considering a contribution. This document explains how to
submit changes, the coding conventions the project uses, and how to
run the test environments locally.

## Getting started

1. Fork the repository on GitHub.
2. Clone your fork and create a feature branch:
   ```
   git clone https://github.com/<your-user>/speedtest-cli.git
   cd speedtest-cli
   git checkout -b my-feature
   ```
3. Install `tox` so you can exercise the test environments:
   ```
   pip install tox
   ```
4. Make your changes, run the tests (see below), and open a pull
   request from your branch.

## Pull requests

Open pull requests against the default development branch of this
repository. Check the GitHub page if you are unsure which branch that
is. Pull requests should be made from a feature branch; do not
submit from a branch named after the target integration branch.

Pull requests will not be accepted that:

1. Do not pass `flake8` (run `tox -e flake8`). `flake8` bundles the
   `pycodestyle` (pep8) and `pyflakes` checks.
2. Do not work with the supported Python versions (see below) or PyPy3.
3. Introduce a **required** runtime dependency outside the Python
   standard library. Optional hardening dependencies (such as
   `defusedxml`, which is detected at import time and falls back to
   the stdlib parser) are acceptable.
4. Are made by editing files via the GitHub website.

## Supported Python versions

All code must support **Python 3.9 and newer**, and PyPy3. Python 2
and Python 3.8 and older are not supported; do not add compatibility
shims for them.

## Dependencies

The script must be usable as a single-file download with zero
third-party runtime dependencies. Any third-party library use must
be optional: guard the import with `try` / `except ImportError`, fall
back to a standard-library implementation, and document the new
optional dependency in `README.rst` and (if applicable) the `setup.py`
extras.

## Coding style

The code is linted with `flake8`, which runs both `pycodestyle` (pep8)
and `pyflakes` under the hood. A few additional conventions are worth
calling out:

1. Do not use `\` for line continuations; wrap long expressions in
   parentheses. `import` statements should each start on their own line
   (`from foo import bar` rather than chained imports).
2. Prefer single quotes (`'`) for string literals, except when the
   string already contains a single quote.
3. Use triple double quotes (`"""..."""`) for docstrings, following
   PEP 257 and PEP 8.
4. Every function, class, and module should have a docstring.
5. Inline comments are for non-obvious intent or surprising invariants,
   not for narrating what the code does.
6. Exceptions raised while handling another exception should use
   `raise NewError(...) from caught_error` so the original traceback
   is preserved explicitly.

## Testing

The project uses `tox` to run environments for each supported
Python version. The default environment compiles the module, runs a
live speed test against speedtest.net, and executes a portable
smoke test of the `--source` error path.

Common commands:

- `tox` — run against every Python interpreter available on the host.
- `tox -e py312` — run against a specific CPython version.
- `tox -e pypy3` — run against PyPy3.
- `tox -e flake8` — lint only (fast, no network).

The live speed test requires internet access to speedtest.net and will
briefly saturate your connection, so prefer `tox -e flake8` for quick
iteration during development.

See `tox.ini` for the exact environment definitions.

## Reporting bugs

Open an issue on the
[GitHub tracker](https://github.com/sivel/speedtest-cli/issues).
Include:

- `speedtest-cli --version` output (which includes the Python version).
- The exact command you ran.
- The full, unredacted error or debug output (run with `--debug` for
  the verbose trace).
- Whether the problem reproduces against multiple servers or is
  isolated to one `--server <id>`.
