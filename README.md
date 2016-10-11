# twitter.py help
```
Usage: twitter.py [OPTIONS]

  Simple tool that uses Twitter API to periodically check in infinite loop
  new tweets satisfying search expression. This tool depends on a
  configuration file which must be provided by the user. The configuration
  file contains Twitter API key and secret properties, that are afterwards
  used for authentication purposes.

Options:
  --config TEXT                 Path to a configuration file with Twitter API
                                keys.
  -s, --search TEXT             Expression to be searched on Twitter.
  -c, --count INTEGER           Count of tweets to be queried during initial
                                wave.
  -i, --interval INTEGER        Interval in seconds specifying time period to
                                query new tweets.
  -v, --verbose                 Show additional output.
  --lang TEXT                   Restricts tweets to the given language, given
                                by an ISO 639-1 code.
  --retweeted / --no-retweeted  Enable or disable showing of retweets.
  --show-id                     Show tweet's ID
  --show-date                   Show tweet's creation date.
  --show-name                   Show tweet's author name.
  --show-screen-name            Show tweet's author twitter nickname.
  --help                        Show this message and exit.
```
# configuration file
In order to be able to properly start twitter wall tool, it is necessary to create configuration file containing OAuth credentials to authenticate into Twitter API. The configuration file has following form:
```
[twitter]
key=XXXXXXXXXX
secret=YYYYYYYYY
```
Of course, *XXXXXXXXXX* and *YYYYYYYYY* must be replaced for correct Twitter API key and secret. Twitter wall tool will implicitly look for configuration file named auth.cfg in executed directory, however this behavior can be changed using *--config* parameter.
