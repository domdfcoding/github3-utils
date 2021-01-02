# Both tests should use the same cassette.


def test_module_cassette_a(module_cassette, github_client):
	github_client.user("domdfcoding")


def test_module_cassette_b(module_cassette, github_client):
	github_client.user("domdfcoding")
