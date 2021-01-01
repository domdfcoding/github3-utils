#!/usr/bin/env python3
#
#  click.py
"""
Extensions for `click <https://click.palletsprojects.com/en/7.x/>`_.

.. versionadded:: 0.2.0
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

# stdlib
from typing import Callable

# 3rd party
import click

__all__ = ["token_option"]


def token_option(token_var: str = "GITHUB_TOKEN") -> Callable:  # nosec: B107
	"""
	Creates a ``-t / --token`` option for the GitHub API token.

	.. versionadded:: 0.2.0

	:param token_var:
	"""

	return click.option(
			"-t",
			"--token",
			type=click.STRING,
			help=(
					"The token to authenticate with the GitHub API. "
					f"Can also be provided via the '{token_var}' environment variable."
					),
			envvar=token_var,
			required=True,
			)
