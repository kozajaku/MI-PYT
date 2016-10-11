import requests
import base64
import click
import configparser
import time
from datetime import datetime

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


def load_twitter_configuration(config_path):
    """Function tries to load key and secret properties from section [twitter] in passed configuration file."""
    config = configparser.ConfigParser()
    config.read(config_path)
    key = config["twitter"]["key"]
    secret = config["twitter"]["secret"]
    return key, secret


def print_tweets(tweets, configuration):
    """Print passed tweets in reverse order (chronologically from the oldest to the newest)."""
    for tweet in reversed(tweets):
        name = screen_name = created = tid = ""
        if configuration["show_name"]:
            name = "Name: {}, ".format(tweet["user"]["name"])
        if configuration["show_screen_name"]:
            screen_name = "Screen name: {}, ".format(tweet["user"]["screen_name"])
        if configuration["show_date"]:
            created = "Created: {}, ".format(datetime.strptime(tweet["created_at"], "%a %b %d %H:%M:%S +0000 %Y")
                                             .strftime("%H:%M:%S %d/%m/%Y"))
        if configuration["show_id"]:
            tid = "Id: {}, ".format(tweet["id"])
        text = "Text: {}".format(tweet["text"])
        click.echo("{}{}{}{}{}\n".format(tid, created, name, screen_name, text))
    # print info if verbose
    if configuration["verbose"]:
        click.echo("* Printed {} tweets in {}".format(len(tweets), time.strftime("%H:%M:%S")))


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


def fetch_tweets(session, params):
    """Function fetches tweets from Twitter API using provided api params."""
    req = session.get("https://api.twitter.com/1.1/search/tweets.json", params=params)
    return req.json()["statuses"]


def initiate_search(session, search, count, interval, configuration):
    """Function initiates tweet fetching in infinite loop."""
    params = {"q": search,
              "count": count}
    # check for lang param
    if "lang" in configuration and configuration["lang"] is not None:
        params["lang"] = configuration["lang"]
    # fetch at most "count" initial tweets
    tweets = fetch_tweets(session, params)
    tweets = filter_tweets(tweets, configuration)
    # print received tweets in reverse order
    print_tweets(tweets, configuration)
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
        tweets = fetch_tweets(session, params)
        fetched_count = len(tweets)
        # if fetched count == 100 it is possible that some tweets were missed - we must check for missed tweets
        while fetched_count == 100:
            params["max_id"] = tweets[-1]["id"] - 1
            older_tweets = fetch_tweets(session, params)
            tweets.extend(older_tweets)
            fetched_count = len(older_tweets)

        # delete max_id from params if exists
        if "max_id" in params:
            del params["max_id"]
        # filter tweets
        tweets = filter_tweets(tweets, configuration)
        # print all collected tweets
        print_tweets(tweets, configuration)
        if len(tweets) != 0:
            last_id = tweets[0]["id"]


@click.command()
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
def twitter_wall(config_path, search, count, interval, **configuration):
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
    try:
        # try to load configuration from passed path
        auth_data = load_twitter_configuration(config_path)
    except KeyError:
        click.echo("Configuration file on path {} is not valid.".format(config_path))
        exit(1)
    else:
        try:
            # get authenticated twitter session using configuration
            session = twitter_session(*auth_data)
            initiate_search(session, search, count, interval, configuration)
        except requests.ConnectionError:
            click.echo("Unable to establish connection to Twitter.")
            exit(1)


if __name__ == "__main__":
    twitter_wall()
