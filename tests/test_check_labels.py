# 3rd party
import pytest
from coincidence.regressions import AdvancedDataRegressionFixture
from github3 import GitHub
from github3.pulls import PullRequest
from github3.repos import Repository

# this package
from github3_utils.check_labels import Label, get_checks_for_pr, label_pr_failures


def test_label_class() -> None:
	label = Label("failure: flake8", "#B60205", "The Flake8 check is failing.")
	assert label.name == "failure: flake8"
	assert label.color == "#B60205"
	assert label.description == "The Flake8 check is failing."

	expected_repr = "Label(name='failure: flake8', color='#B60205', description='The Flake8 check is failing.')"
	assert repr(label) == expected_repr
	assert str(label) == "failure: flake8"

	assert label.to_dict() == {
			"name": "failure: flake8",
			"color": "#B60205",
			"description": "The Flake8 check is failing.",
			}


@pytest.mark.usefixtures("cassette")
def test_creation_on_repo(github_client: GitHub) -> None:

	repo = github_client.repository("domdfcoding", "repo_helper_demo")

	current_labels = {label.name: label for label in repo.labels()}
	assert "failure: flake8" not in current_labels

	label = Label("failure: flake8", "#B60205", "The Flake8 check is failing.")

	label.create(repo)

	repo = github_client.repository("domdfcoding", "repo_helper_demo")
	current_labels = {label.name: label for label in repo.labels()}
	assert "failure: flake8" in list(current_labels.keys())


@pytest.mark.usefixtures("module_cassette")
def test_get_checks_for_pr(
		github_client: GitHub,
		advanced_data_regression: AdvancedDataRegressionFixture,
		) -> None:
	repo: Repository = github_client.repository("sphinx-toolbox", "sphinx-autofixture")
	pull: PullRequest = repo.pull_request(10)

	checks = get_checks_for_pr(pull)
	advanced_data_regression.check({k: sorted(v) for k, v in checks._asdict().items()})


@pytest.mark.usefixtures("module_cassette")
def test_label_pr_failures(github_client: GitHub) -> None:
	repo: Repository = github_client.repository("sphinx-toolbox", "sphinx-autofixture")
	pull: PullRequest = repo.pull_request(10)

	labels = label_pr_failures(pull)
	assert sorted(labels) == ["failure: Linux", "failure: Windows"]
