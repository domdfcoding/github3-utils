# stdlib
import os

# 3rd party
import pytest
from betamax import Betamax  # type: ignore[import]
from coincidence.regressions import AdvancedDataRegressionFixture
from github3 import GitHub
from github3.exceptions import AuthenticationFailed
from github3.repos import Repository

# this package
from github3_utils import Impersonate, get_repos, get_user, iter_repos


def test_get_user(
		advanced_data_regression: AdvancedDataRegressionFixture,
		github_client: GitHub,
		) -> None:
	with Betamax(github_client.session) as vcr:
		vcr.use_cassette("test_get_user", record="once")

		advanced_data_regression.check(get_user(github_client).as_dict())


def test_get_user_no_auth() -> None:
	github = GitHub('')

	with Betamax(github.session) as vcr:
		vcr.use_cassette("test_get_user_no_auth", record="once")

		with pytest.raises(AuthenticationFailed):
			get_user(github)


def test_impersonate() -> None:
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


class TestGetRepos:

	@pytest.mark.usefixtures("cassette")
	def test_get_repos(
			self,
			github_client: GitHub,
			advanced_data_regression: AdvancedDataRegressionFixture,
			) -> None:
		user = github_client.user("domdfcoding")
		advanced_data_regression.check([repo.name for repo in get_repos(user)])

	@pytest.mark.usefixtures("cassette")
	def test_get_repos_full(self, github_client: GitHub) -> None:
		user = github_client.user("domdfcoding")

		repo: Repository
		for repo in get_repos(user, full=True):
			assert isinstance(repo, Repository)

	@pytest.mark.usefixtures("cassette")
	def test_get_repos_org(
			self,
			github_client: GitHub,
			advanced_data_regression: AdvancedDataRegressionFixture,
			) -> None:
		user = github_client.organization("sphinx-toolbox")
		advanced_data_regression.check([repo.name for repo in get_repos(user)])


class TestIterRepos:

	@pytest.mark.usefixtures("cassette")
	def test_get_repos(
			self,
			github_client: GitHub,
			advanced_data_regression: AdvancedDataRegressionFixture,
			) -> None:
		advanced_data_regression.check([repo.name for repo in iter_repos(github_client, ["domdfcoding"])])

	@pytest.mark.usefixtures("cassette")
	def test_get_repos_org(
			self,
			github_client: GitHub,
			advanced_data_regression: AdvancedDataRegressionFixture,
			) -> None:
		repos = [repo.name for repo in iter_repos(github_client, orgs=["sphinx-toolbox"])]
		advanced_data_regression.check(repos)
