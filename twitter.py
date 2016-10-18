import requests
import base64
import click
import configparser
import time
from datetime import datetime
import flask
from flask import g

app = flask.Flask(__name__)

class WebConfiguration:
    def __init__(self):



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
        if configuration["verbose"]:
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
        if configuration["verbose"]:
            click.echo("* Filtered {} tweets.".format(filtered))
        return tweets

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
            created = "Created: {}, ".format(datetime.strptime(tweet["created_at"], "%a %b %d %H:%M:%S %z %Y")
                                             .strftime("%H:%M:%S %d/%m/%Y"))
        if configuration["show_id"]:
            tid = "Id: {}, ".format(tweet["id"])
        text = "Text: {}".format(tweet["text"])
        return "{}{}{}{}{}\n".format(tid, created, name, screen_name, text)

    def continually_print_tweets(self, search, count, interval, configuration):
        """Print formated stream of tweets from tweet_stream."""
        for tweet in self.tweet_stream(search, count, interval, configuration):
            click.echo(self.tweet_console_format(tweet, configuration))


@app.route("/search")
def search_page():
    # redirect back to home page if search query is not valid
    if "q" not in flask.request.args:
        return flask.redirect(flask.url_for("index_page"))
    q_param = flask.request.args["q"].strip()
    if len(q_param) == 0:
        return flask.redirect(flask.url_for("index_page"))

    # q_param is valid here
    # detect retweet param
    filter_retweeted = False
    if "filter-retweeted" in flask.request.args and flask.request.args["filter-retweeted"] == "on":
        filter_retweeted = True
    # create twitter wall instance
    twitter_wall = TwitterWall()



@app.route("/")
def index_page():
    return flask.render_template("index.html")


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
@click.option("--config", "config_path", default="auth.cfg", help="Path to a configuration file with Twitter API keys.")
def web(debug):
    # setup debug flags if debug
    if debug:
        app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(debug=debug)


if __name__ == "__main__":
    # do some flask debug flag settings
    cli()
