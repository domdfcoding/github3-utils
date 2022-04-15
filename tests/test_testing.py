# 3rd party
import pytest
from github3 import GitHub

# Both tests should use the same cassette.


@pytest.mark.usefixtures("module_cassette")
def test_module_cassette_a(github_client: GitHub) -> None:
	github_client.user("domdfcoding")


@pytest.mark.usefixtures("module_cassette")
def test_module_cassette_b(github_client: GitHub) -> None:
	github_client.user("domdfcoding")
