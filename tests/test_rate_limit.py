# 3rd party
import pytest
from coincidence import AdvancedFileRegressionFixture
from github3 import GitHub

# this package
from github3_utils import RateLimitExceeded, echo_rate_limit


@pytest.mark.usefixtures("cassette")
def test_rate_limit(
		capsys,
		advanced_file_regression: AdvancedFileRegressionFixture,
		github_client: GitHub,
		) -> None:
	with echo_rate_limit(github_client):
		pass

	advanced_file_regression.check(capsys.readouterr().out)


@pytest.mark.usefixtures("cassette")
def test_rate_limit_exceeded(capsys, github_client: GitHub) -> None:
	with pytest.raises(
			RateLimitExceeded,
			match="No requests available! Resets at 2020-12-31 00:04:05",
			):

		with echo_rate_limit(github_client):
			pass
