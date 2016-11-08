Console
=======

For information about how to use **twitterjk** *console* command, you can call it with ``--help`` argument::

    twitterjk console --help

Output::

    Usage: twitterjk console [OPTIONS]

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

Example usage 1
---------------

Following command specifies, that I want to look for *wikileaks* keyword, I want to show date and id of tweets and I
do not wont to show retweets::

    twitterjk console -s wikileaks --no-retweeted --show-date --show-id

Example output::

    Id: 796117601210531840, Created: 23:30:01 08/11/2016, Text: WikiLeaks se défend d'avoir été manipulé par la Russie https://t.co/CHrFXjWgvQ https://t.co/YdQzOHoubK

    Id: 796117601541820416, Created: 23:30:02 08/11/2016, Text: Thank you @wikileaks &amp; mr. Assange for waking up so many Americans to the truth! You have helped the world #UniteAgainstCorruption

    Id: 796117604523970560, Created: 23:30:02 08/11/2016, Text: @jongaunt @talk2meradiouk Meanwhile, this is happening. https://t.co/m9NJ3SIyRI

    Id: 796117611008311296, Created: 23:30:04 08/11/2016, Text: @lionheart_james @MelBchREALTOR I suppose this Wikileaks release of 2 of her  intelligence officers is fake too? https://t.co/fI8sF7Brtf

    ...

Example usage 2
---------------

Following command specifies, that I have configuration file named ``test.cfg`` in folder named ``config``, during first
fetch I want to get only 5 tweets and I want to check for new tweets every 5 seconds. I am looking for keyword *python*::

    twitterjk console --search python --config config/test.cfg -c 5 -i 5

Example output::

    Text: RT @MrPatCake: Hmm. The guy who made millions laugh with Monty Python or the guy who hacked Nigel Havers' phone when he was nursing his dyi…

    Text: Mike Driscoll: Python 201 is the Featured Book on Leanpub Today https://t.co/jlb6OOfdY6 https://t.co/yXFSyujkUg

    Text: I added a video to a @YouTube playlist https://t.co/PKyIHJf7o1 More on list comp and generators - Intermediate Python Programming p.5

    Text: RT @egreen460: https://t.co/aWH3qw9Gnx is For Sale #programming #nodejs #clojure #perl #reactjs #angularjs #jquery #html5 #css3 #ruby #pyth…

    Text: RT @MrPatCake: Hmm. The guy who made millions laugh with Monty Python or the guy who hacked Nigel Havers' phone when he was nursing his dyi…

    Text: #PHP #Python Wurk raises $1 million to help cannabis companies manage their people https://t.co/nu908bkWC2 #techn… https://t.co/Z6UXWQQNGC

    Text: RT @MrPatCake: Hmm. The guy who made millions laugh with Monty Python or the guy who hacked Nigel Havers' phone when he was nursing his dyi…

    Text: Choosing the Right Back-end Technology for your Business https://t.co/ir3kQGh6eE #Ruby #Python #Java #Strategy https://t.co/illsViOUiZ

    Text: RT @HYPEBEAST: Check out @TheShoeSurgeon as he serves up a python-clad @VLONE x @Nike Air Force 1.
    https://t.co/kWEN6nO3li https://t.co/KZ…

    Text: Python list: if a pair of numbers equals 0 return the positions of the elements
    https://t.co/sUcvOmnOUq
    #python #nested-lists

    Text: PythonQnA: Usage of __slots__? #python https://t.co/lst68L3khn : Usage of __slots__?… https://t.co/z5SkCHvvMQ… https://t.co/oP9LdrJ0vh

    ...

