#!/usr/bin/env python3
#
#  check_labels.py
"""
Helpers for creating labels to mark pull requests with which tests are failing.

.. versionadded:: 0.4.0
"""
#
#  Copyright © 2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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
from typing import Dict, List

# 3rd party
import attr
import github3.issues.label
from domdf_python_tools.doctools import prettify_docstrings
from github3.repos import Repository

__all__ = ["Label", "check_status_labels"]


@prettify_docstrings
@attr.s
class Label:
	"""
	Represents a issue or pull request label.
	"""

	#: The text of the label.
	name: str = attr.ib(converter=str)

	#: The background colour of the label.
	color: str = attr.ib(converter=str)

	#: A short description of the label.
	description: str = attr.ib(default=None)

	def __str__(self) -> str:
		return self.name

	def to_dict(self) -> Dict[str, str]:
		"""
		Return the :class:`~.Label` as a dictionary.
		"""

		return {
				"name": self.name,
				"color": self.color,
				"description": self.description,
				}

	def create(self, repo: Repository) -> github3.issues.label.Label:
		"""
		Create this label on the given repository.

		:param repo:
		"""

		return repo.create_label(**self.to_dict())


check_status_labels: List[Label] = [
		Label("failure: flake8", "#B60205", "The Flake8 check is failing."),
		Label("failure: mypy", "#DC1C13", "The mypy check is failing."),
		Label("failure: docs", "#EA4C46", "The docs check is failing."),
		Label("failure: Windows", "#F07470", "The Windows tests are failing."),
		Label("failure: Linux", "#F6BDC0", "The Linux tests are failing."),
		Label("failure: Multiple", "#D93F0B", "Multiple checks are failing."),
		]
"""
List of labels corresponding to failing pull request checks.
"""

# Multiple is used if three or more categories failing
