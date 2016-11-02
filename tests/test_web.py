from twitterjk import twitter
import pytest
import betamax
import os


def sanitize_token(interaction, current_cassette):
    from betamax.cassette import cassette
    # sanitize request
    reqAuth = interaction.data["request"]["headers"]["Authorization"]
    if reqAuth:
        current_cassette.placeholders.append(
                cassette.Placeholder(placeholder="<AUTH_REQUEST>", replace=reqAuth[0])
        )
    # sanitize response - if correct
    if interaction.data["response"]["status"]["code"] != 200:
        return
    respAuth = interaction.data["response"]["body"]["string"]
    if respAuth and interaction.data["request"]["uri"] == "https://api.twitter.com/oauth2/token":
        current_cassette.placeholders.append(
                cassette.Placeholder(placeholder="<AUTH_TOKEN>", replace=respAuth)
        )


with betamax.Betamax.configure() as config:
    config.cassette_library_dir = 'tests/fixtures/cassettes'
    config.before_record(callback=sanitize_token)
    if "AUTH_FILE" in os.environ:
        config.default_cassette_options["record_mode"] = "all"
    else:
        config.default_cassette_options["record_mode"] = "none"

    @pytest.fixture
    def twitterjk(betamax_session):
        betamax_session.headers.update({'Accept-Encoding': 'identity'})
        if "AUTH_FILE" in os.environ:
            config_path = os.environ["AUTH_FILE"]
            key, secret = twitter.parse_configuration(config_path)
            session = twitter.twitter_session(key, secret, betamax_session)
        else:
            session = betamax_session
        from twitterjk.twitter import app
        app.config["TESTING"] = True
        app.config['TWITTER_WALL'] = twitter.TwitterWall(session)
        return app.test_client()


def test_index_page(twitterjk):
    """Test whether index page "/" works properly"""
    resp = twitterjk.get("/")
    assert resp.status_code == 200
    data = resp.data.decode("utf-8")
    assert "<h1>Twitter Wall</h1>" in data


@pytest.mark.parametrize("page", ("nonehere", "/nonehere", "/foo/bar"))
def test_non_existing_pages(twitterjk, page):
    """Test whether it properly returns Not Found for nonexistent pages"""
    resp = twitterjk.get(page)
    assert resp.status_code == 404


@pytest.mark.parametrize("query", (
        ("python", "python"),
        ("%23wikileaks", "#wikileaks"),
        ("%40YouTube", "@YouTube")))
def test_search_page(twitterjk, query):
    """Test whether search page works properly"""
    resp = twitterjk.get("/search?q={}".format(query[0]))
    assert resp.status_code == 200
    data = resp.data.decode("utf-8")
    assert "<h1>Search results for query: <i>{}</i></h1>".format(query[1]) in data


def test_missing_query(twitterjk):
    """Test whether it properly redirects back to index when there is no q param"""
    resp = twitterjk.get("/search")
    assert resp.status_code == 302


def test_hiding_retweets(twitterjk):
    """Test whether retweets are truly hidden"""
    resp = twitterjk.get("/search?q=%40YouTube&filter-retweeted=on")
    assert resp.status_code == 200
    data = resp.data.decode("utf-8")
    assert "<div class=\"value\">RT <a" not in data


def test_impossible_query(twitterjk):
    """Test whether retweets are truly hidden"""
    resp = twitterjk.get("/search?q=thisissomeimpossiblesearchfoobar")
    assert resp.status_code == 200
    data = resp.data.decode("utf-8")
    assert "<h2>No tweets were found!</h2>" in data
