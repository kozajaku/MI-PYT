Web
===

For information about how to use **twitterjk** *web* command, you can call it with ``--help`` argument::

    twitterjk web --help

Output::

    Usage: twitterjk web [OPTIONS]

      Web frontend for Twitter Wall tool. User can query specified twitter
      search expression on simple web page and show results in simple format
      including all additional tweet entities.

    Options:
      --debug         Setup debug flags for Flask application.
      --port INTEGER  TCP port of the web server.
      --host TEXT     The hostname to listen on.
      --config TEXT   Path to a configuration file with Twitter API keys.
      --help          Show this message and exit.

Example usage
-------------

In order to start the server listening on all interfaces and on port ``9999`` execute::

    twitterjk web --host 0.0.0.0 --port 9999

You can now open your web browser and connect to the server on `localhost:9999 <http://localhost:9999>`_. **twitterjk**
web GUI consists of two pages:

Pages structure
---------------

- ``/`` - page with simple query form
- ``/search?q=<query>&filter-retweeted=<filter>`` - page providing searched results

``<query>`` stands for searched query string. Note that is is necessary to properly URL escape this parameter if it
contains special characters like ``#`` or ``@``.

``<filter>`` parameter defines whether retweets should be filtered. Values can be either ``on`` or ``off``, whereas if
you omit this parameter, ``off`` value is automatically passed.
