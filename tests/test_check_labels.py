# 3rd party
from github3.pulls import PullRequest
from github3.repos import Repository
from pytest_regressions.data_regression import DataRegressionFixture

# this package
from github3_utils.check_labels import Label, get_checks_for_pr, label_pr_failures


def test_label_class():
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


def test_creation_on_repo(cassette, github_client):

	repo = github_client.repository("domdfcoding", "repo_helper_demo")

	current_labels = {label.name: label for label in repo.labels()}
	assert "failure: flake8" not in current_labels

	label = Label("failure: flake8", "#B60205", "The Flake8 check is failing.")

	label.create(repo)

	repo = github_client.repository("domdfcoding", "repo_helper_demo")
	current_labels = {label.name: label for label in repo.labels()}
	assert "failure: flake8" in list(current_labels.keys())


def test_get_checks_for_pr(module_cassette, github_client, data_regression: DataRegressionFixture):
	repo: Repository = github_client.repository("sphinx-toolbox", "sphinx-autofixture")
	pull: PullRequest = repo.pull_request(10)

	checks = get_checks_for_pr(pull)
	data_regression.check({k: sorted(v) for k, v in checks._asdict().items()})


def test_label_pr_failures(module_cassette, github_client):
	repo: Repository = github_client.repository("sphinx-toolbox", "sphinx-autofixture")
	pull: PullRequest = repo.pull_request(10)

	labels = label_pr_failures(pull)
	assert sorted(labels) == ["failure: Linux", "failure: Windows"]
