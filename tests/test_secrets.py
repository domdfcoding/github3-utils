# 3rd party
import pytest
from apeye import URL
from coincidence.regressions import AdvancedDataRegressionFixture
from github3 import GitHub

# this package
from github3_utils.secrets import build_secrets_url, encrypt_secret, get_public_key, get_secrets, set_secret


@pytest.mark.usefixtures("module_cassette")
def test_build_secrets_url(github_client: GitHub) -> None:
	repo = github_client.repository("domdfcoding", "repo_helper_demo")
	secrets_url = build_secrets_url(repo)

	assert isinstance(secrets_url, URL)
	assert secrets_url == URL("https://api.github.com/repos/domdfcoding/repo_helper_demo/actions/secrets")


@pytest.mark.usefixtures("module_cassette")
def test_get_public_key(
		advanced_data_regression: AdvancedDataRegressionFixture,
		github_client: GitHub,
		) -> None:
	repo = github_client.repository("domdfcoding", "repo_helper_demo")
	advanced_data_regression.check(get_public_key(repo))


@pytest.mark.usefixtures("cassette")
def test_get_secrets(
		advanced_data_regression: AdvancedDataRegressionFixture,
		github_client: GitHub,
		) -> None:
	repo = github_client.repository("domdfcoding", "repo_helper_demo")
	advanced_data_regression.check(get_secrets(repo))


@pytest.mark.usefixtures("module_cassette")
def test_encrypt_secret(
		advanced_data_regression: AdvancedDataRegressionFixture,
		github_client: GitHub,
		) -> None:
	repo = github_client.repository("domdfcoding", "repo_helper_demo")

	public_key = get_public_key(repo)

	secret = encrypt_secret(public_key["key"], "Hello World")
	assert secret.endswith('=')
	assert len(secret) == 80


@pytest.mark.usefixtures("module_cassette")
def test_set_secret(
		advanced_data_regression: AdvancedDataRegressionFixture,
		github_client: GitHub,
		) -> None:
	repo = github_client.repository("domdfcoding", "repo_helper_demo")

	public_key = get_public_key(repo)

	response = set_secret(repo, "GREETING", "Hello World", public_key)
	assert response.status_code == 201
