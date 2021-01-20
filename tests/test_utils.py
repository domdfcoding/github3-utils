# stdlib
import os

# 3rd party
import pytest
from betamax import Betamax  # type: ignore
from github3 import GitHub
from github3.exceptions import AuthenticationFailed
from github3.repos import Repository
from pytest_regressions.data_regression import DataRegressionFixture

# this package
from github3_utils import Impersonate, get_repos, get_user


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


def test_get_repos(github_client, cassette, data_regression):
	user = github_client.user("domdfcoding")
	data_regression.check([repo.name for repo in get_repos(user)])


def test_get_repos_full(github_client, cassette, data_regression):
	user = github_client.user("domdfcoding")

	repo: Repository
	for repo in get_repos(user, full=True):
		assert isinstance(repo, Repository)


def test_get_repos_org(github_client, cassette, data_regression):
	user = github_client.organization("sphinx-toolbox")
	data_regression.check([repo.name for repo in get_repos(user)])
