# 3rd party
import pytest
from betamax import Betamax  # type: ignore
from domdf_python_tools.testing import check_file_regression
from github3 import GitHub  # type: ignore

# this package
from github3_utils import RateLimitExceeded, echo_rate_limit


def test_rate_limit(capsys, file_regression):
	github = GitHub(token="FAKE_TOKEN")

	with Betamax(github.session) as vcr:
		vcr.use_cassette("rate_limit", record="once")

		with echo_rate_limit(github):
			pass

		check_file_regression(capsys.readouterr().out, file_regression)


def test_rate_limit_exceeded(capsys, file_regression):
	github = GitHub(token="FAKE_TOKEN")

	with Betamax(github.session) as vcr:
		vcr.use_cassette("rate_limit_exceeded", record="once")

		with pytest.raises(  # noqa: PT012
			RateLimitExceeded,
			match="No requests available! Resets at 2020-12-31 00:04:05",
			):
			with echo_rate_limit(github):
				pass
