# stdlib
import datetime
from typing import Optional

# 3rd party
import pytest
from betamax import Betamax  # type: ignore[import-untyped]
from coincidence.regressions import AdvancedDataRegressionFixture, AdvancedFileRegressionFixture
from domdf_python_tools.stringlist import StringList
from github3 import GitHub

# this package
from github3_utils.apps import iter_installed_repos, make_footer_links

# This is a fake key generated from https://travistidwell.com/jsencrypt/demo/
FAKE_KEY = StringList([
		"-----YEK ETAVIRP ASR NIGEB-----"[::-1],
		"MIICXgIBAAKBgQDNdKST4/dcvrnOFw5fCzoaU3hBIj6xoDmB12GMbWALlaztU8R6",
		"0mQN36kNGqTMVP3JUaE5S3Pe1NBoZJku8eyo4fwZknblC7+rk59fNo5hAc/MdX5O",
		"23W81DODokYvhafZDfHsUwf91BBiSQFWCMzsL3vB5tU/6l4Q0agb2t0JKQIDAQAB",
		"AoGBAI8nlwT08oZM3moa5oiS6gkt37yCf+yEF43A5NdT3ngz8inrFBwAPHbuQHxA",
		"9FLrZWnA1vV0/WdmIVCbx6BOMPa6+0cb1XZBaUI0FZJwoJqroVLBeiufd5E+Jcyd",
		"13BH1g/2V0bRJ8QOKMXlZAzIGabqBGwjNDXf+M/cRa/1SCmBAkEA92XweDnMT6bj",
		"nHOlmcyopa5jL3xLd3FdSDVOolFMyNUm/lHvLKpOn+Ue3SnYs8Wb+TiKz5we2cf8",
		"qy9pY8ejGwJBANSZYMP3v3IwFR8LCcSn0teUDh+5SKx5yOkmgtZ+OZHpWHjj/xNy",
		"jhJe0T7B3CpLwknA2TkglyyrVpanRZlkhQsCQQDr35FJzzFwr9lLDSfSX0Jb1MxU",
		"Ndlt4/PgKJL0RzdCM5ed2liC6U1VPYoTqxYlMD7penM+RcdUNEw+mlGNBIYJAkAt",
		"ly6fF7PgYttEqvNPTsXyIPfeabdh9UPWa8HHCY6C8c1dL1d17iz1V4v7r0rtbw2d",
		"D1QF4i1JEP0ilYBhYqL9AkEApRbo7po5k57CVAIS+Ur9v/b1eMl0iPr4RHBLBU5f",
		"VcINCgSAYARRcs1kVPyBMwFRu+oc1D5AtfcKaqxCx8apGw==",
		"-----END RSA PRIVATE KEY-----",
		])


def test_iter_installed_repos(advanced_data_regression: AdvancedDataRegressionFixture) -> None:
	github = GitHub()

	GITHUBAPP_ID = 89426
	GITHUBAPP_KEY = str(FAKE_KEY).encode("UTF-8")

	with Betamax(github.session) as vcr:
		vcr.use_cassette("test_iter_installed_repos", record="once")

		repo_names = []

		for repo in iter_installed_repos(
				client=github,
				private_key_pem=GITHUBAPP_KEY,
				app_id=GITHUBAPP_ID,
				):
			repo_names.append(repo["full_name"])

		advanced_data_regression.check(repo_names)


def test_iter_installed_repos_errors() -> None:

	error_msg = "Either 'context_switcher' or all of 'client', 'private_key_pem' and 'app_id' must be provided."

	with pytest.raises(ValueError, match=error_msg):
		next(iter_installed_repos())

	with pytest.raises(ValueError, match=error_msg):
		next(iter_installed_repos(private_key_pem=b"helloworld"))

	with pytest.raises(ValueError, match=error_msg):
		next(iter_installed_repos(app_id=1234))

	with pytest.raises(ValueError, match=error_msg):
		next(iter_installed_repos(client=GitHub()))


@pytest.mark.usefixtures("fixed_datetime")
@pytest.mark.parametrize("event_date", [datetime.date(2020, 12, 25), datetime.date(2020, 7, 4), None])
def test_make_footer_links_marketplace(
		advanced_file_regression: AdvancedFileRegressionFixture,
		event_date: Optional[datetime.date],
		) -> None:

	footer = make_footer_links(
			"domdfcoding",
			"octocheese",
			event_date=event_date,
			type="marketplace",
			docs_url="https://octocheese.readthedocs.io"
			)

	advanced_file_regression.check(footer)

	footer = make_footer_links(
			"domdfcoding", "octocheese", event_date=event_date, docs_url="https://octocheese.readthedocs.io"
			)

	advanced_file_regression.check(footer)

	if event_date is not None:
		event_date = datetime.datetime(event_date.year, event_date.month, event_date.day)

		footer = make_footer_links(
				"domdfcoding",
				"octocheese",
				event_date=event_date,
				type="marketplace",
				docs_url="https://octocheese.readthedocs.io"
				)

		advanced_file_regression.check(footer)

		footer = make_footer_links(
				"domdfcoding", "octocheese", event_date=event_date, docs_url="https://octocheese.readthedocs.io"
				)

		advanced_file_regression.check(footer)


@pytest.mark.usefixtures("fixed_datetime")
@pytest.mark.parametrize(
		"event_date",
		[
				datetime.date(2020, 12, 25),
				datetime.date(2020, 7, 4),
				datetime.date(2022, 4, 15),
				datetime.date(2022, 10, 28),
				None,
				],
		)
def test_make_footer_links_app(
		advanced_file_regression: AdvancedFileRegressionFixture,
		event_date: Optional[datetime.date],
		) -> None:

	footer = make_footer_links(
			"domdfcoding",
			"repo-helper-bot",
			event_date=event_date,
			type="app",
			docs_url=None,
			)

	advanced_file_regression.check(footer)

	footer = make_footer_links(
			"domdfcoding",
			"repo-helper-bot",
			event_date=event_date,
			type="app",
			)

	advanced_file_regression.check(footer)

	if event_date is not None:
		event_date = datetime.datetime(event_date.year, event_date.month, event_date.day)

		footer = make_footer_links(
				"domdfcoding",
				"repo-helper-bot",
				event_date=event_date,
				type="app",
				docs_url=None,
				)

		advanced_file_regression.check(footer)

		footer = make_footer_links(
				"domdfcoding",
				"repo-helper-bot",
				event_date=event_date,
				type="app",
				)

		advanced_file_regression.check(footer)
