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
import re
from typing import Dict, NamedTuple, Set, Union

# 3rd party
import attr
import github3.issues.label
from domdf_python_tools.doctools import prettify_docstrings
from github3.checks import CheckRun
from github3.issues import Issue
from github3.pulls import PullRequest, ShortPullRequest
from github3.repos import Repository
from github3.repos.commit import ShortCommit

__all__ = ["Label", "check_status_labels", "Checks", "get_checks_for_pr", "label_pr_failures"]


@prettify_docstrings
@attr.s(frozen=True, slots=True)
class Label:
	"""
	Represents an issue or pull request label.
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


check_status_labels: Dict[str, Label] = {
		label.name: label
		for label in [
				Label("failure: flake8", "#B60205", "The Flake8 check is failing."),
				Label("failure: mypy", "#DC1C13", "The mypy check is failing."),
				Label("failure: docs", "#EA4C46", "The docs check is failing."),
				Label("failure: Windows", "#F07470", "The Windows tests are failing."),
				Label("failure: Linux", "#F6BDC0", "The Linux tests are failing."),
				# Label("failure: Multiple", "#D93F0B", "Multiple checks are failing."),
				]
		}
"""
Labels corresponding to failing pull request checks.
"""

# The ``failure: Multiple`` label is used if three or more categories failing.


class Checks(NamedTuple):
	"""
	Represents the sets of status checks returned by :func:`~.get_checks_for_pr`.
	"""

	successful: Set[str]
	failing: Set[str]
	running: Set[str]
	skipped: Set[str]
	neutral: Set[str]


def get_checks_for_pr(pull: Union[PullRequest, ShortPullRequest]) -> Checks:
	"""
	Returns a :class:`~.Checks` object containing sets of check names grouped by their status.

	:param pull: The pull request to obtain checks for.
	"""

	head_commit: ShortCommit = list(pull.commits())[-1]

	failing = set()
	running = set()
	successful = set()
	skipped = set()
	neutral = set()

	check_run: CheckRun
	for check_run in head_commit.check_runs():

		if check_run.status in {"queued", "running", "in_progress"}:
			running.add(check_run.name)
		elif check_run.conclusion in {"failure", "cancelled", "timed_out", "action_required"}:
			failing.add(check_run.name)
		elif check_run.conclusion == "success":
			successful.add(check_run.name)
		elif check_run.conclusion == "skipped":
			skipped.add(check_run.name)
		elif check_run.conclusion == "neutral":
			neutral.add(check_run.name)

	# Remove failing checks from successful etc. (as all checks appear twice for PRs)
	successful = successful - failing - running
	running = running - failing
	skipped = skipped - running - failing - successful
	neutral = neutral - running - failing - successful

	return Checks(
			successful=successful,
			failing=failing,
			running=running,
			skipped=skipped,
			neutral=neutral,
			)


_python_dev_re = re.compile(r".*Python\s*\d+\.\d+.*(dev|alpha|beta|rc).*", flags=re.IGNORECASE)


def label_pr_failures(pull: Union[PullRequest, ShortPullRequest]) -> Set[str]:
	"""
	Labels the given pull request to indicate which checks are failing.

	:param pull:

	:return: The new labels set for the pull request.
	"""

	pr_checks = get_checks_for_pr(pull)

	failure_labels: Set[str] = set()
	success_labels: Set[str] = set()

	def determine_labels(from_: Set[str], to: Set[str]) -> None:
		for check in from_:
			if _python_dev_re.match(check):
				continue

			if check in {"Flake8", "docs"}:
				to.add(f"failure: {check.lower()}")
			elif check.startswith("mypy"):
				to.add("failure: mypy")
			elif check.startswith("ubuntu"):
				to.add("failure: Linux")
			elif check.startswith("windows"):
				to.add("failure: Windows")

	determine_labels(pr_checks.failing, failure_labels)
	determine_labels(pr_checks.successful, success_labels)

	issue: Issue = pull.issue()

	current_labels = {label.name for label in issue.labels()}

	for label in success_labels:
		if label in current_labels and label not in failure_labels:
			issue.remove_label(label)

	current_labels -= success_labels
	current_labels.update(failure_labels)

	issue.add_labels(*current_labels)

	return current_labels
