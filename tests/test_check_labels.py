# this package
from github3_utils.check_labels import Label


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
