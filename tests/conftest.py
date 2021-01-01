# 3rd party
import pytest
from _pytest.fixtures import FixtureRequest
from betamax import Betamax  # type: ignore
from domdf_python_tools.paths import PathPlus
from github3 import GitHub  # type: ignore

with Betamax.configure() as config:
	config.cassette_library_dir = PathPlus(__file__).parent / "cassettes"

pytest_plugins = ("domdf_python_tools.testing", )


@pytest.fixture()
def github_client() -> GitHub:
	return GitHub(token="FAKE_TOKEN")  # nosec: B106


@pytest.fixture()
def cassette(request: FixtureRequest, github_client):
	with Betamax(github_client.session) as vcr:
		vcr.use_cassette(request.node.name, record="none")

		yield github_client
