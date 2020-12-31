#!/usr/bin/env python3
#
#  secrets.py
"""
Functions for setting and updating GitHub Actions secrets.
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
from base64 import b64encode

# 3rd party
from apeye import URL
from github3.repos import Repository  # type: ignore
from nacl import encoding, public  # type: ignore
from requests import Response

# this package
from github3_utils._typing import make_typed_dict

__all__ = [
		"build_secrets_url",
		"encrypt_secret",
		"get_public_key",
		"get_secrets",
		"set_secret",
		"PublicKey",
		]


def build_secrets_url(repo: Repository) -> URL:
	"""
	Returns the URL via which secrets can be checked and set.

	:param repo: The repository to check/set secrets for.
	"""

	return URL(repo._build_url("actions/secrets", base_url=repo._api))


_PublicKey = make_typed_dict("_PublicKey", {"ETag": str, "Last-Modified": str}, total=False)


class PublicKey(_PublicKey):
	"""
	:class:`typing.TypedDict` representing the return type of :func:`~.get_public_key`.
	"""

	key: str
	key_id: str


def get_public_key(repo: Repository) -> "PublicKey":
	"""
	Returns the public key used to encrypt secrets for the given repository.

	:param repo: The repository the secrets are to be set for.
	"""

	response = repo._get(str(build_secrets_url(repo) / "public-key"), headers=repo.PREVIEW_HEADERS)
	public_key = repo._json(response, 200)

	return public_key


def get_secrets(repo: Repository):
	"""
	Returns a list of secret names for the given repository.

	:param repo:
	"""

	secrets_url = build_secrets_url(repo)
	raw_secrets = repo._json(repo._get(str(secrets_url), headers=repo.PREVIEW_HEADERS), 200)

	return [secret["name"] for secret in raw_secrets["secrets"]]


def encrypt_secret(public_key: str, secret_value: str) -> str:
	"""
	Encrypt a GitHub Actions secret.

	:param public_key:
	:param secret_value:

	If the key has been obtained with :func:`~.get_secrets` then ``public_key`` will be:

	.. code-block:: python

		get_secrets(repo)['key']
	"""

	public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
	sealed_box = public.SealedBox(public_key)
	encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
	return b64encode(encrypted).decode("utf-8")


def set_secret(
		repo: Repository,
		secret_name: str,
		value: str,
		public_key: "PublicKey",
		) -> Response:
	"""
	Set the value of the given secret.

	:param repo:
	:param secret_name:
	:param value:
	:param public_key:
	"""

	encrypted_value = encrypt_secret(
			public_key["key"],
			secret_value=value,
			)

	key_id = public_key["key_id"]
	secret_json = {"encrypted_value": encrypted_value, "key_id": key_id}
	response = repo._put(
			str(build_secrets_url(repo) / secret_name),
			headers=repo.PREVIEW_HEADERS,
			json=secret_json,
			)

	return response
