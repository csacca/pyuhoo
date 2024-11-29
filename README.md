Forked version of pyUhoo which fixes the login problem.

This can be integrated with your existing plugin by updating the manifest file requirements line
to depend on this repository: `pyuhoo@git+https://github.com/wrouesnel/pyuhoo.git@master#0.0.6a2`

# pyuhoo

[![PyPi version](https://img.shields.io/pypi/v/pyuhoo.svg)](https://pypi.python.org/pypi/pyuhoo/)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/csacca/pyuhoo/master.svg)](https://results.pre-commit.ci/latest/github/csacca/pyuhoo/master)
![ci workflow](https://github.com/csacca/pyuhoo/actions/workflows/ci.yaml/badge.svg)

Python API for talking to uHoo consumer API

Please note that this is a non-public API that has been reverse-engineered from mobile
apps. It is likely to break unexpectedly when uHoo changes the API.
