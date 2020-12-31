# 3rd party
from betamax import Betamax  # type: ignore
from domdf_python_tools.paths import PathPlus

with Betamax.configure() as config:
	config.cassette_library_dir = PathPlus(__file__).parent / "cassettes"

pytest_plugins = ("domdf_python_tools.testing", )
