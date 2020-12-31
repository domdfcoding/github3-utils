# 3rd party
import pytest
from betamax import Betamax  # type: ignore
from domdf_python_tools.paths import PathPlus
from github3 import GitHub  # type: ignore

with Betamax.configure() as config:
	config.cassette_library_dir = PathPlus(__file__).parent / "cassettes"

pytest_plugins = ("domdf_python_tools.testing", )


@pytest.fixture()
def github_client() -> GitHub:
	return GitHub(token="FAKE_TOKEN")  # nosec: B106
