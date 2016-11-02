from twitterjk import twitter
import flexmock
import pytest
import builtins
from io import StringIO

key = "keyaaabbbcccddd"
secret = "secretaaabbbcccddaaabbbcccddd"

correct_config = """
[twitter]
key = {}
secret = {}
""".format(key, secret)

incorrect_config1 = """
[twitter]
keya = {}
secret = {}
""".format(key, secret)

incorrect_config2 = """
[twitter]
key = {}
secrett = {}
""".format(key, secret)

incorrect_config3 = """
[twittter]
key = {}
secret = {}
""".format(key, secret)


def exit_mock(expected):
    def assertion(received):
        assert expected == received

    return assertion


def test_correct_config():
    """Test whether config parser properly parses configuration file"""
    flexmock(builtins, open=StringIO(correct_config))
    res_key, res_secret = twitter.parse_configuration("some_path")
    assert res_key == key
    assert res_secret == secret


@pytest.mark.parametrize("config", (incorrect_config1, incorrect_config2, incorrect_config3))
def test_incorrect_config(config):
    """Test whether config parser fails parsing upon mistyped configuration files"""
    # should do exit(1)
    flexmock(builtins, open=StringIO(config))
    with pytest.raises(SystemExit) as id:
        twitter.parse_configuration("some_path")
    assert id.value.code == 1


@pytest.mark.parametrize("config", ("some_path.txt", "auth.cfg", "../auth.cfg", "someFolder/test.txt"))
def test_path_opening(config):
    """Test whether it truly tries to open passed config path"""

    def check_path_opening(path, **other):
        assert path == config
        return StringIO(correct_config)

    flexmock(builtins, open=check_path_opening)
    twitter.parse_configuration(config)
