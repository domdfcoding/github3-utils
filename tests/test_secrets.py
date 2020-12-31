# 3rd party
import pytest
from apeye import URL
from betamax import Betamax  # type: ignore
from pytest_regressions.data_regression import DataRegressionFixture

# this package
from github3_utils.secrets import build_secrets_url, encrypt_secret, get_public_key, get_secrets, set_secret


@pytest.fixture()
def secrets_test_cassette(github_client):
	with Betamax(github_client.session) as vcr:
		vcr.use_cassette("test_secrets", record="none")

		yield github_client


def test_build_secrets_url(github_client, secrets_test_cassette):
	repo = github_client.repository("domdfcoding", "repo_helper_demo")
	secrets_url = build_secrets_url(repo)

	assert isinstance(secrets_url, URL)
	assert secrets_url == URL("https://api.github.com/repos/domdfcoding/repo_helper_demo/actions/secrets")


def test_get_public_key(data_regression: DataRegressionFixture, github_client, secrets_test_cassette):
	repo = github_client.repository("domdfcoding", "repo_helper_demo")
	data_regression.check(get_public_key(repo))


def test_get_secrets(data_regression: DataRegressionFixture, github_client, cassette):
	repo = github_client.repository("domdfcoding", "repo_helper_demo")
	data_regression.check(get_secrets(repo))


def test_encrypt_secret(data_regression: DataRegressionFixture, github_client, secrets_test_cassette):
	repo = github_client.repository("domdfcoding", "repo_helper_demo")

	public_key = get_public_key(repo)

	secret = encrypt_secret(public_key["key"], "Hello World")
	assert secret.endswith('=')
	assert len(secret) == 80


def test_set_secret(data_regression: DataRegressionFixture, github_client, secrets_test_cassette):
	repo = github_client.repository("domdfcoding", "repo_helper_demo")

	public_key = get_public_key(repo)

	response = set_secret(repo, "GREETING", "Hello World", public_key)
	assert response.status_code == 201
