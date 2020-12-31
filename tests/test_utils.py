# stdlib
import os

# 3rd party
import pytest
from betamax import Betamax  # type: ignore
from github3 import GitHub  # type: ignore
from github3.exceptions import AuthenticationFailed  # type: ignore
from pytest_regressions.data_regression import DataRegressionFixture

# this package
from github3_utils import Impersonate, get_user


def test_get_user(data_regression: DataRegressionFixture, github_client):
	with Betamax(github_client.session) as vcr:
		vcr.use_cassette("test_get_user", record="once")

		data_regression.check(get_user(github_client).as_dict())


def test_get_user_no_auth(data_regression: DataRegressionFixture):
	github = GitHub('')

	with Betamax(github.session) as vcr:
		vcr.use_cassette("test_get_user_no_auth", record="once")

		with pytest.raises(AuthenticationFailed):
			get_user(github)


def test_impersonate():
	name = "repo-helper[bot]"
	email = f"74742576+{name}@users.noreply.github.com"

	commit_as_bot = Impersonate(
			name=name,
			email=email,
			)

	assert os.environ.get("GIT_COMMITTER_NAME", '') != name
	assert os.environ.get("GIT_COMMITTER_EMAIL", '') != email
	assert os.environ.get("GIT_AUTHOR_NAME", '') != name
	assert os.environ.get("GIT_AUTHOR_EMAIL", '') != email

	with commit_as_bot():
		assert os.environ["GIT_COMMITTER_NAME"] == name
		assert os.environ["GIT_COMMITTER_EMAIL"] == email
		assert os.environ["GIT_AUTHOR_NAME"] == name
		assert os.environ["GIT_AUTHOR_EMAIL"] == email

	assert os.environ.get("GIT_COMMITTER_NAME", '') != name
	assert os.environ.get("GIT_COMMITTER_EMAIL", '') != email
	assert os.environ.get("GIT_AUTHOR_NAME", '') != name
	assert os.environ.get("GIT_AUTHOR_EMAIL", '') != email
