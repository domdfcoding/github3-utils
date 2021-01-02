#!/usr/bin/env python3
#
#  testing.py
"""
Fixtures for `pytest <https://docs.pytest.org/en/stable/>`_.

.. extras-require:: testing
	:__pkginfo__:

.. versionadded:: 0.2.0

To use this module you need to add, at a minimum, the following to your ``conftest.py``:

.. code-block:: python

	from betamax import Betamax

	pytest_plugins = ("github3_utils.testing", )

	with Betamax.configure() as config:
		config.cassette_library_dir = "<path to cassettes directory>"
"""
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# 3rd party
import pytest  # nodep
from _pytest.fixtures import FixtureRequest  # nodep
from betamax import Betamax  # type: ignore  # nodep
from github3 import GitHub  # type: ignore

__all__ = ["cassette", "github_client", "module_cassette"]


@pytest.fixture()
def github_client() -> GitHub:
	"""
	Provides an instance of :class:`github3.github.GitHub`,
	using a fake token to authenticate.
	"""  # noqa: D400

	return GitHub(token="FAKE_TOKEN")  # nosec: B106


@pytest.fixture()
def cassette(request: FixtureRequest, github_client):
	"""
	Provides a Betamax cassette scoped to the test function
	which record and plays back interactions with the GitHub API.
	"""  # noqa: D400

	with Betamax(github_client.session) as vcr:
		vcr.use_cassette(request.node.name, record="none")

		yield github_client


@pytest.fixture()
def module_cassette(request: FixtureRequest, github_client):
	"""
	Provides a Betamax cassette scoped to the test module
	which record and plays back interactions with the GitHub API.
	"""  # noqa: D400

	cassette_name = request.module.__name__.split('.')[-1]

	with Betamax(github_client.session) as vcr:
		# print(f"Using cassette {cassette_name!r}")
		vcr.use_cassette(cassette_name, record="none")

		yield github_client
