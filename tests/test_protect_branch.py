# 3rd party
import pytest
from github3 import GitHub
from github3.repos import Repository
from github3.repos.branch import Branch, BranchProtection

# this package
from github3_utils import protect_branch


@pytest.mark.usefixtures("cassette")
def test_protect_branch(github_client: GitHub) -> None:
	repo: Repository = github_client.repository("domdfcoding", "repo_helper_demo")
	branch: Branch = repo.branch("master")

	required_checks = [
			"Python 3.6",
			"Python 3.7",
			"mypy",
			"Flake8",
			"pre-commit.ci - push",
			]

	assert protect_branch(branch, required_checks)
	assert branch.protected

	branch = repo.branch("master")
	assert branch.protected

	protection: BranchProtection = branch.protection()

	assert list(protection.required_status_checks.contexts()) == [
			"Python 3.6",
			"Python 3.7",
			"mypy",
			"Flake8",
			"pre-commit.ci - push",
			]
