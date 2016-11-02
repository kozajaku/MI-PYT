import flexmock
import pytest
from twitterjk import twitter
from click.testing import CliRunner


@pytest.fixture
def runner():
    return CliRunner()


@pytest.mark.parametrize("count", (-10, -5, -1, 101, 200, 5000))
def test_count_boundary_fail(runner, count):
    """Test whether count parsing fails when out of interval <0, 100>"""
    flexmock(twitter, parse_configuration=lambda path: exit(100))
    result = runner.invoke(twitter.cli, ["console", "--count", count, "--search", "python"])
    assert result.exit_code == 1


@pytest.mark.parametrize("count", range(101))
def test_count_boundary_succ(runner, count):
    """Test whether count parsing succeeds when in interval <0, 100>"""
    flexmock(twitter, parse_configuration=lambda path: exit(100))
    result = runner.invoke(twitter.cli, ["console", "--count", count, "--search", "python"])
    assert result.exit_code == 100


@pytest.mark.parametrize("interval", (-5000, -50, -10, -5, -2, -1, 0))
def test_interval_limit_fail(runner, interval):
    """Test whether interval cannot be less than 1"""
    flexmock(twitter, parse_configuration=lambda path: exit(100))
    result = runner.invoke(twitter.cli, ["console", "--interval", interval, "--search", "python"])
    assert result.exit_code == 1


@pytest.mark.parametrize("interval", (1, 2, 3, 4, 10, 50, 100, 5000))
def test_interval_limit_succ(runner, interval):
    """Test whether interval succeeds when greater or equal 1"""
    flexmock(twitter, parse_configuration=lambda path: exit(100))
    result = runner.invoke(twitter.cli, ["console", "--interval", interval, "--search", "python"])
    assert result.exit_code == 100


def test_default_parameters(runner):
    """Test that start with default parameters (count, interval) is working"""
    flexmock(twitter, parse_configuration=lambda path: exit(100))
    result = runner.invoke(twitter.cli, ["console", "--search", "python"])
    assert result.exit_code == 100


@pytest.mark.parametrize("config", ("auth.cfg", "something", "wtf.txt", "../../konf.cnf", "somefolder/conf/config.txt"))
def test_config_passing(runner, config):
    """Test whether config path is properly passed to parse_configuration"""

    def check_config_path(path):
        assert path == config
        exit(100)

    flexmock(twitter, parse_configuration=check_config_path)
    result = runner.invoke(twitter.cli, ["console", "--search", "python", "--config", config])
    assert result.exit_code == 100  # just to be sure


def test_config_default_passing(runner):
    """Test whether config path is properly passed to parse_configuration"""

    def check_config_path(path):
        assert path == "auth.cfg"  # default config
        exit(100)

    flexmock(twitter, parse_configuration=check_config_path)
    result = runner.invoke(twitter.cli, ["console", "--search", "python"])
    assert result.exit_code == 100  # just to be sure
