#!/usr/bin/env python3
#
#  __init__.py
"""
Handy utilities for `github3.py <https://github3py.readthedocs.io/en/master/>`_.
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
#  "protect_branch" based on github3.py
#  Copyright (c) 2012-2016 by Ian Cordasco
#  |  Redistribution and use in source and binary forms, with or without
#  |  modification, are permitted provided that the following conditions are
#  |  met:
#  |
#  |  1. Redistributions of source code must retain the above copyright
#  |  notice, this list of conditions and the following disclaimer.
#  |  2. Redistributions in binary form must reproduce the above copyright
#  |  notice, this list of conditions and the following disclaimer in the
#  |  documentation and/or other materials provided with the distribution.
#  |  3. The name of the author may not be used to endorse or promote products
#  |  derived from this software without specific prior written permission.
#  |
#  |  THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
#  |  IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#  |  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  |  DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
#  |  INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#  |  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#  |  SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
#  |  HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
#  |  STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
#  |  ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#  |  POSSIBILITY OF SUCH DAMAGE.
#

# stdlib
import datetime
import os
from contextlib import contextmanager
from typing import Iterable, Iterator, List, Optional, Union, overload

# 3rd party
import attr
from apeye import URL
from click import echo
from github3 import GitHub
from github3.orgs import Organization
from github3.repos import Repository, ShortRepository
from github3.repos.branch import Branch
from github3.users import User
from typing_extensions import Literal

# this package
from github3_utils.headers import LUKE_CAKE

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2020 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "0.6.1"
__email__: str = "dominic@davis-foster.co.uk"

__all__ = [
		"RateLimitExceeded",
		"echo_rate_limit",
		"get_user",
		"protect_branch",
		"Impersonate",
		"get_repos",
		"iter_repos",
		]


class RateLimitExceeded(RuntimeError):
	"""
	Custom exception class to indicate the GitHub rate limit has been exceeded and no further requests should be made.
	"""

	#: The time at which the rate limit will be reset.
	reset_time: datetime.datetime

	def __init__(self, reset_time: datetime.datetime):
		super().__init__(f"No requests available! Resets at {reset_time}")
		self.reset_time = reset_time


@contextmanager
def echo_rate_limit(github: GitHub, verbose: bool = True) -> Iterator[GitHub]:
	"""
	Contextmanager to echo the GitHub API rate limit before and after making a series of requests.

	:param github:
	:param verbose: If :py:obj:`False` no output will be printed.

	:raises: :exc:`click.Abort` if the rate limit has been exceeded.
	"""

	rate = github.rate_limit()["rate"]
	remaining_requests = rate["remaining"]
	reset = datetime.datetime.fromtimestamp(rate["reset"])

	if not remaining_requests:
		raise RateLimitExceeded(reset)

	if verbose:
		echo(f"{remaining_requests} requests available.")

	yield github

	if verbose:
		rate = github.rate_limit()["rate"]
		new_remaining_requests = rate["remaining"]
		used_requests = remaining_requests - new_remaining_requests
		reset = datetime.datetime.fromtimestamp(rate["reset"])

		echo(f"Used {used_requests} requests. {new_remaining_requests} remaining. Resets at {reset}")


def get_user(github: GitHub) -> User:
	"""
	Retrieve a :class:`github3.users.User` object for the authenticated user.

	:param github:
	"""

	url = github._build_url("user")
	json = github._json(github._get(url), 200)
	return github._instance_or_null(User, json)


def protect_branch(branch: Branch, status_checks: Optional[List[str]] = None) -> bool:
	"""
	Enable force push protection and configure status check enforcement.

	:param branch: The branch to enable protection for.
	:param status_checks: A list of strings naming status checks which must pass before merging.
		Use :py:obj:`None` or omit to use the already associated value.

	:returns: :py:obj:`True` if successful, :py:obj:`False` otherwise.
	"""

	previous_values = None
	previous_protection = getattr(branch, "original_protection", {})

	if previous_protection:
		previous_values = previous_protection.get("required_status_checks", {})

	if status_checks is None and previous_values:
		status_checks = previous_values["contexts"]

	edit = {
			"required_status_checks": {"strict": False, "contexts": status_checks},
			"enforce_admins": None,
			"required_pull_request_reviews": {
					"dismiss_stale_reviews": False,
					"required_approving_review_count": 1,
					},
			"restrictions": None,
			}

	resp = branch._put(
			str(URL(branch._api) / "protection"),
			json=edit,
			headers=LUKE_CAKE,
			)

	if branch._boolean(resp, 200, 404):
		branch.protected = True
		return True
	else:  # pragma: no cover
		return False


@attr.s
class Impersonate:
	"""
	Context manager to make commits as a specific user.

	Sets the following environment variables:

	* ``GIT_COMMITTER_NAME``
	* ``GIT_COMMITTER_EMAIL``
	* ``GIT_AUTHOR_NAME``
	* ``GIT_AUTHOR_EMAIL``

	.. attention::

		Any changes to environment variables made during the scope
		of the context manager will be reset on exit.

	.. latex:clearpage::

	:bold-title:`Example:`

	.. code-block:: python

		name = "repo-helper[bot]"
		email = f"74742576+{name}@users.noreply.github.com"

		commit_as_bot = Impersonate(name=name, email=email)

		with commit_as_bot():
			...

	"""

	#: The name of the committer.
	name: str = attr.ib()

	#: The email address of the committer.
	email: str = attr.ib()

	@contextmanager
	def __call__(self) -> Iterator[None]:
		"""
		The context manager itself.
		"""

		_environ = dict(os.environ)  # or os.environ.copy()

		try:
			name = "repo-helper[bot]"
			email = f"74742576+{name}@users.noreply.github.com"

			os.environ["GIT_COMMITTER_NAME"] = name
			os.environ["GIT_COMMITTER_EMAIL"] = email
			os.environ["GIT_AUTHOR_NAME"] = name
			os.environ["GIT_AUTHOR_EMAIL"] = email

			yield

		finally:
			os.environ.clear()
			os.environ.update(_environ)


@overload
def get_repos(
		user_or_org: Union[User, Organization],
		full: Literal[True],
		) -> Iterator[Repository]: ...


@overload
def get_repos(
		user_or_org: Union[User, Organization],
		full: Literal[False] = ...,
		) -> Iterator[ShortRepository]: ...


def get_repos(
		user_or_org: Union[User, Organization],
		full: bool = False,
		) -> Union[Iterator[Repository], Iterator[ShortRepository]]:
	"""
	Returns an iterator over the user or organisation's repositories.

	.. versionadded:: 0.5.0

	:param user_or_org:
	:param full: If :py:obj:`True` yields :class:`~github3.repos.repo.Repository` objects.
		Otherwise, yields :class:`~github3.repos.repo.ShortRepository` objects
	"""

	url = user_or_org._build_url("users", user_or_org.login, "repos")
	params = {"type": "owner", "sort": "full_name", "direction": "asc"}

	for repo in user_or_org._iter(-1, url, ShortRepository, params):
		if full:
			yield repo.refresh()
		else:
			yield repo


def iter_repos(
		github: GitHub,
		users: Iterable[str] = (),
		orgs: Iterable[str] = (),
		) -> Iterator[ShortRepository]:
	"""
	Returns an iterator over the repositories belonging to all ``users`` and all ``orgs``.

	.. versionadded:: 0.5.0

	:param github:
	:param users: An iterable of usernames to fetch the repositories for.
	:param orgs: An iterable of organization names to fetch the repositories for.
	"""

	for user in users:
		_user: Optional[User] = github.user(user)
		if _user is None:
			raise ValueError(f"No such user {user}")

		yield from get_repos(_user, full=False)

	for org in orgs:
		_org: Optional[Organization] = github.organization(org)

		if _org is None:
			raise ValueError(f"No such organization {org}")

		yield from get_repos(_org, full=False)
