#!/usr/bin/env python3
#
#  apps.py
"""
Functions and classes for GitHub apps.
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
from typing import Dict, Iterator, Optional

# 3rd party
import attr
from github3 import GitHub  # type: ignore
from github3.apps import Installation  # type: ignore

__all__ = ["ContextSwitcher", "iter_installed_repos"]


@attr.s
class ContextSwitcher:
	"""
	Class to aid switching contexts between the app itself and its installations.
	"""

	#:
	client: GitHub = attr.ib()

	#: The bytes of the private key for this GitHub App.
	private_key_pem: bytes = attr.ib()

	#: The integer identifier for this GitHub App.
	app_id: int = attr.ib()

	def login_as_app(self):
		"""
		Login as the GitHub app.
		"""

		self.client.login_as_app(self.private_key_pem, self.app_id)

	def login_as_user_installation(self, username: str) -> int:
		"""
		Login as a user installation of a GitHub app, and return its installation ID.

		:param username:
		"""

		# Log in as installation for this user
		installation_id = self.client.app_installation_for_user(username).id
		self.client.login_as_app_installation(self.private_key_pem, self.app_id, installation_id)

		return installation_id

	def login_as_repo_installation(self, owner: str, repository: str) -> int:
		"""
		Login as a repository installation of a GitHub app, and return its installation ID.

		:param owner:
		:param repository:
		"""

		installation_id = self.client.app_installation_for_repository(
				owner=owner,
				repository=repository,
				).id
		self.client.login_as_app_installation(self.private_key_pem, self.app_id, installation_id)

		return installation_id


def iter_installed_repos(
		*,
		context_switcher: Optional[ContextSwitcher] = None,
		client: Optional[GitHub] = None,
		private_key_pem: Optional[bytes] = None,
		app_id: Optional[int] = None,
		) -> Iterator[Dict]:
	"""
	Returns an iterator over all repositories the app is installed for.

	:param context_switcher: A :class:`~.ContextSwitcher` used to switch contexts
		between the app itself and its installations.
	:param client: The bytes of the private key for this GitHub App.
	:param private_key_pem: The bytes of the private key for this GitHub App.
	:param app_id: The integer identifier for this GitHub App.

	Either ``context_switcher`` or all of ``client``, ``private_key_pem`` and ``app_id`` must be provided.
	"""

	if context_switcher is None:
		if client is None or private_key_pem is None or app_id is None:
			raise ValueError(
					"Either 'context_switcher' or all of 'client', "
					"'private_key_pem' and 'app_id' must be provided.",
					)
		else:
			context_switcher = ContextSwitcher(client, private_key_pem, app_id)

	context_switcher.login_as_app()

	installation: Installation
	for installation in client.app_installations(context_switcher.app_id):  # type: ignore
		# print(installation)
		# print(installation.account)
		username = installation.account["login"]

		context_switcher.login_as_app()
		context_switcher.login_as_user_installation(username)

		# Get repositories for this user.

		headers = {
				**installation.session.headers,
				"Accept": "application/vnd.github.machine-man-preview+json",
				}

		def get_page(page: int = 1):
			return context_switcher.client.session.get(  # type: ignore
				installation.repositories_url,
				params={"per_page": 100, "page": page},
				headers=headers,  # pylint: disable=cell-var-from-loop
				).json()

		response = get_page()
		total_repos = response["total_count"]
		yield from response["repositories"]

		total_repos -= len(response["repositories"])
		page = 2

		while total_repos > 0:
			response = get_page(page)
			page += 1
			yield from response["repositories"]
			total_repos -= len(response["repositories"])
