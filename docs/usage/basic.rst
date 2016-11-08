Basic usage
===========

After :doc:`../installation/installation` you have two ways to start the **twitterjk** tool. Either you invoke::

    python -m twitterjk command args

or directly ::

    twitterjk command args

**twitterjk** nowadays support two following commands:

- console - Running the whole tool in the console. See :doc:`console`
- web - Starting web server listening on the specified port which serves as a web GUI. See :doc:`web`

You can find more information about arguments by calling **twitterjk** with ``--help`` argument::

    Usage: twitterjk [OPTIONS] COMMAND [ARGS]...

    Options:
      --help  Show this message and exit.

    Commands:
      console  Simple tool that uses Twitter API to...
      web      Web frontend for Twitter Wall tool.
