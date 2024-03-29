# 3rd party
import click
from click.testing import CliRunner, Result
from coincidence.regressions import AdvancedFileRegressionFixture
from consolekit import click_command

# this package
from github3_utils.click import token_option


def test_token_option(
		monkeypatch,
		advanced_file_regression: AdvancedFileRegressionFixture,
		) -> None:

	@token_option()
	@click_command()
	def demo(token: str) -> None:
		click.echo(f"The token is: {token}")

	runner = CliRunner()

	result: Result = runner.invoke(demo, catch_exceptions=False, args=["-t", "FAKE_TOKEN"])
	assert result.stdout == "The token is: FAKE_TOKEN\n"

	result = runner.invoke(demo, catch_exceptions=False, args=["--token", "FAKE_TOKEN"])
	assert result.stdout == "The token is: FAKE_TOKEN\n"

	monkeypatch.setenv("GITHUB_TOKEN", "FAKE_TOKEN")
	result = runner.invoke(demo, catch_exceptions=False)
	assert result.stdout == "The token is: FAKE_TOKEN\n"

	result = runner.invoke(demo, catch_exceptions=False, args=["--help"])
	advanced_file_regression.check(result.stdout.rstrip())


def test_token_option_alt_name(
		monkeypatch,
		advanced_file_regression: AdvancedFileRegressionFixture,
		) -> None:

	@token_option("MA_TOKEN")
	@click_command()
	def demo(token: str) -> None:
		click.echo(f"The token is: {token}")

	runner = CliRunner()

	result: Result = runner.invoke(demo, catch_exceptions=False, args=["-t", "FAKE_TOKEN"])
	assert result.stdout == "The token is: FAKE_TOKEN\n"

	result = runner.invoke(demo, catch_exceptions=False, args=["--token", "FAKE_TOKEN"])
	assert result.stdout == "The token is: FAKE_TOKEN\n"

	monkeypatch.setenv("MA_TOKEN", "FAKE_TOKEN")
	result = runner.invoke(demo, catch_exceptions=False)
	assert result.stdout == "The token is: FAKE_TOKEN\n"

	result = runner.invoke(demo, catch_exceptions=False, args=["--help"])
	advanced_file_regression.check(result.stdout.rstrip())
