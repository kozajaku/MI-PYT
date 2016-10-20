import requests
import base64
import click
import configparser
import time
from datetime import datetime, timezone
import flask
import urllib.parse

app = flask.Flask(__name__)
app.config["config_path"] = "auth.cfg"


class TwitterWall:
    def __init__(self, api_key, api_secret):
        """Constructor assigns new twitter session into instance"""
        self.session = self.twitter_session(api_key, api_secret)

    @staticmethod
    def twitter_session(api_key, api_secret):
        """Function creates new http session with properly assigned Authorization header."""
        session = requests.Session()
        secret = '{}:{}'.format(api_key, api_secret)
        secret64 = base64.b64encode(secret.encode('ascii')).decode('ascii')

        headers = {
            'Authorization': 'Basic {}'.format(secret64),
            'Host': 'api.twitter.com',
        }

        r = session.post('https://api.twitter.com/oauth2/token',
                         headers=headers,
                         data={'grant_type': 'client_credentials'})

        bearer_token = r.json()['access_token']

        def bearer_auth(req):
            req.headers['Authorization'] = 'Bearer ' + bearer_token
            return req

        session.auth = bearer_auth
        return session

    def fetch_tweets(self, params, configuration):
        """Function fetches tweets from Twitter API using provided api params."""
        req = self.session.get("https://api.twitter.com/1.1/search/tweets.json", params=params)
        # print info if verbose
        if "verbose" in configuration and configuration["verbose"]:
            click.echo("* Fetched {} tweets in {}".format(len(req.json()["statuses"]), time.strftime("%H:%M:%S")))
        return req.json()["statuses"]

    @staticmethod
    def filter_tweets(tweets, configuration):
        """Function provides filtering in tweets collection"""
        filtered = len(tweets)
        if not configuration["retweeted"]:
            tweets = filter(lambda t: "retweeted_status" not in t, tweets)

        tweets = list(tweets)
        filtered = filtered - len(tweets)

        # print info if verbose
        if "verbose" in configuration and configuration["verbose"]:
            click.echo("* Filtered {} tweets.".format(filtered))
        return tweets

    def tweet_single_fetch(self, search, count, configuration):
        """Function fetches count tweets, filters them and return for the purpose of web app"""
        params = {"q": search,
                  "count": count}
        return self.filter_tweets(self.fetch_tweets(params, configuration), configuration)

    def tweet_stream(self, search, count, interval, configuration):
        """Function fetches tweets in infinite loop and yields their generator"""
        params = {"q": search,
                  "count": count}
        # check for lang param
        if "lang" in configuration and configuration["lang"] is not None:
            params["lang"] = configuration["lang"]
        # fetch at most "count" initial tweets
        tweets = self.fetch_tweets(params, configuration)
        tweets = self.filter_tweets(tweets, configuration)
        # yield initial tweet collection in reverse order
        yield from reversed(tweets)
        # setup count api argument to maximum allowed value
        params["count"] = 100
        # setup variable for since_id api argument
        last_id = 1  # last seen tweet id
        if len(tweets) != 0:
            last_id = tweets[0]["id"]
        # periodically do: sleep "interval" seconds and then fetch new tweets
        while True:
            time.sleep(interval)

            # set since_id api argument
            params["since_id"] = last_id
            tweets = self.fetch_tweets(params, configuration)
            fetched_count = len(tweets)
            # if fetched count == 100 it is possible that some tweets were missed - we must check for missed tweets
            while fetched_count == 100:
                params["max_id"] = tweets[-1]["id"] - 1
                older_tweets = self.fetch_tweets(params, configuration)
                tweets.extend(older_tweets)
                fetched_count = len(older_tweets)

            # delete max_id from params if exists
            if "max_id" in params:
                del params["max_id"]
            # filter tweets
            tweets = self.filter_tweets(tweets, configuration)
            if len(tweets) != 0:
                last_id = tweets[0]["id"]
            # yield tweets in reverse order and repeat
            yield from reversed(tweets)

    @staticmethod
    def tweet_console_format(tweet, configuration):
        """Method formats tweet for printing into console"""
        name = screen_name = created = tid = ""
        if configuration["show_name"]:
            name = "Name: {}, ".format(tweet["user"]["name"])
        if configuration["show_screen_name"]:
            screen_name = "Screen name: {}, ".format(tweet["user"]["screen_name"])
        if configuration["show_date"]:
            created = "Created: {}, ".format(convert_time(tweet["created_at"]))
        if configuration["show_id"]:
            tid = "Id: {}, ".format(tweet["id"])
        text = "Text: {}".format(tweet["text"])
        return "{}{}{}{}{}\n".format(tid, created, name, screen_name, text)

    def continually_print_tweets(self, search, count, interval, configuration):
        """Print formatted stream of tweets from tweet_stream."""
        for tweet in self.tweet_stream(search, count, interval, configuration):
            click.echo(self.tweet_console_format(tweet, configuration))


@app.route("/search")
def search_page():
    """If properly parsed parameters from http get method, renders resulting tweets."""
    # redirect back to home page if search query is not valid
    if "q" not in flask.request.args:
        return flask.redirect(flask.url_for("index_page"))
    q_param = flask.request.args["q"].strip()
    if len(q_param) == 0:
        return flask.redirect(flask.url_for("index_page"))

    # q_param is valid here
    # detect retweet param
    configuration = {"retweeted": True}
    if "filter-retweeted" in flask.request.args and flask.request.args["filter-retweeted"] == "on":
        configuration["retweeted"] = False
    # create twitter wall instance
    twitter_wall = TwitterWall(*parse_configuration(app.config["config_path"]))
    # fetch maximum number of tweets (100 max defined by Twitter API
    tweets = twitter_wall.tweet_single_fetch(q_param, 100, configuration)
    return flask.render_template("search.html", tweets=tweets, query=q_param)


@app.route("/")
def index_page():
    """Render index page where the search form is shown."""
    return flask.render_template("index.html")


@app.template_filter('time')
def convert_time(passed_time):
    """Convert the Twitter time format to own type"""
    return datetime.strptime(passed_time, "%a %b %d %H:%M:%S %z %Y").replace(tzinfo=timezone.utc). \
        astimezone(tz=None).strftime("%H:%M:%S %d/%m/%Y")


def create_link(href, text, as_search=False):
    if as_search:
        escaped_href = urllib.parse.quote_plus(href)
        return "<a href=\"/search?q={}\">{}</a>".format(escaped_href, text)
    else:
        return "<a href=\"{}\">{}</a>".format(href, text)


@app.template_filter('user_mentions')
def create_user_mentions(mentions):
    """Convert user_mention entities into readable format"""
    return ", ".join(
            map(lambda m: create_link("@" + m["screen_name"], "{} (@{})".format(m["name"], m["screen_name"]), True),
                mentions))


@app.template_filter('hashtags')
def create_hashtags(hashtags):
    """Convert hashtag entities into readable format"""
    return ", ".join(map(lambda h: create_link("#" + h["text"], "#" + h["text"], True), hashtags))


@app.template_filter('urls')
def create_urls(urls):
    """Convert url entities into readable format"""
    return ", ".join(map(lambda u: create_link(u["expanded_url"], u["expanded_url"]), urls))


@app.template_filter('symbols')
def create_urls(symbols):
    """Convert symbol entities into readable format"""
    return ", ".join(map(lambda s: s["text"], symbols))


@app.template_filter("image")
def create_image(src, size=None):
    if size is None:
        return "<image src=\"{}\" />".format(src)
    else:
        return "<image src=\"{}:{}\" />".format(src, size)


@app.template_filter('media')
def create_media(media):
    """Convert media entities into readable format"""
    return "\n".join(map(lambda m: create_image(m["media_url"], "small"), media))


@app.template_filter('textWithEntities')
def text_with_entities(tweet):
    """Enrich tweet text using twitter entities."""
    text = tweet["text"]
    entities = tweet["entities"]
    indices_map = {}
    # hashtag indices
    for hashtag in entities["hashtags"]:
        indices_map[hashtag["indices"][0]] = (hashtag["indices"][1], lambda tmp: create_link(tmp, tmp, True))
    # mention indices
    for mention in entities["user_mentions"]:
        indices_map[mention["indices"][0]] = (mention["indices"][1], lambda tmp: create_link(tmp, tmp, True))
    # url indices
    for url in entities["urls"]:
        indices_map[url["indices"][0]] = (url["indices"][1], lambda tmp: create_link(url["expanded_url"], tmp))
    # symbol indices
    for symbol in entities["symbols"]:
        indices_map[symbol["indices"][0]] = (symbol["indices"][1], lambda tmp: create_link(tmp, tmp, True))
    result = ""
    i = 0
    next_to_read = 0
    while i < len(text):
        if i in indices_map:
            index_tuple = indices_map[i]
            if i > next_to_read:
                result += text[next_to_read:i]
            result += index_tuple[1](text[i:index_tuple[0]])
            i = index_tuple[0] - 1
            next_to_read = i + 1
        i += 1
    if i > next_to_read:
        result += text[next_to_read:i]

    return result


def parse_configuration(config_path):
    """Function tries to load key and secret properties from section [twitter] in passed configuration file."""
    try:
        config = configparser.ConfigParser()
        config.read(config_path)
        key = config["twitter"]["key"]
        secret = config["twitter"]["secret"]
    except KeyError:
        click.echo("Configuration file on path {} is not valid.".format(config_path))
        exit(1)
    else:
        return key, secret


@click.group()
def cli():
    pass


@cli.command()
@click.option("--config", "config_path", default="auth.cfg", help="Path to a configuration file with Twitter API keys.")
@click.option("-s", "--search", prompt="Search expression", help="Expression to be searched on Twitter.")
@click.option("-c", "--count", default=20, help="Count of tweets to be queried during initial wave.")
@click.option("-i", "--interval", default=10, help="Interval in seconds specifying time period to query new tweets.")
@click.option("-v", "--verbose", is_flag=True, help="Show additional output.")
@click.option("--lang", help="Restricts tweets to the given language, given by an ISO 639-1 code.")
@click.option("--retweeted/--no-retweeted", default=True, help="Enable or disable showing of retweets.")
@click.option("--show-id", is_flag=True, help="Show tweet's ID")
@click.option("--show-date", is_flag=True, help="Show tweet's creation date.")
@click.option("--show-name", is_flag=True, help="Show tweet's author name.")
@click.option("--show-screen-name", is_flag=True, help="Show tweet's author twitter nickname.")
def console(config_path, search, count, interval, **configuration):
    """Simple tool that uses Twitter API to periodically check in infinite loop new tweets satisfying
    search expression. This tool depends on a configuration file which must be provided by the user. The configuration
    file contains Twitter API key and secret properties, that are afterwards used for authentication purposes."""
    # do some value checking
    if count < 0 or count >= 100:
        click.echo("Invalid count value. Count must not be negative and it must not be greater than 100.")
        exit(1)
    if interval < 1:
        click.echo("Invalid interval value. Interval must be greater than 0.")
        exit(1)
    # try to load configuration from passed path
    auth_data = parse_configuration(config_path)
    try:
        # get authenticated twitter session using configuration
        twitter_wall = TwitterWall(*auth_data)
        twitter_wall.continually_print_tweets(search, count, interval, configuration)
    except requests.ConnectionError:
        click.echo("Unable to establish connection to Twitter.")
        exit(1)


@cli.command()
@click.option("--debug", is_flag=True, help="Setup debug flags for Flask application.")
@click.option("--port", default=5000, help="TCP port of the web server.")
@click.option("--host", default="127.0.0.1", help="The hostname to listen on.")
@click.option("--config", "config_path", default="auth.cfg", help="Path to a configuration file with Twitter API keys.")
def web(debug, port, host, config_path):
    """Web frontend for Twitter Wall tool. User can query specified twitter search expression on simple web page and
     show results in simple format including all additional tweet entities."""
    # setup path to configuration file
    app.config["config_path"] = config_path
    # setup debug flags if debug
    if debug:
        app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(debug=debug, port=port, host=host)


if __name__ == "__main__":
    # do some flask debug flag settings
    cli()
