Testing
=======

To invoke tests simply execute following command which will automatically download necessary testing dependencies
and invoke tests::

    python3 setup.py test

If the dependencies are already installed in your environment, you can also directly use ``pytest`` command::

    pytest tests

Following testing dependencies are nowadays necessary to run tests:

- flexmock
- pytest
- betamax

betamax
-------

In order to be able to run tests even when you are offline or you do not have Twitter API credentials, testing
uses betamax framework to record *http* communication into cassettes. During testing these cassettes are used instead
of initiating communication with Twitter server. You can however create new cassettes with new communication session
whenever you want.

To invoke new cassettes recording for betamax testing, simply setup new
environment variable named ``AUTH_FILE`` pointing to the path to a
configuration file with valid credentials (see :doc:`../installation/config`). For instance, to start
testing by recording new cassettes, invoke::

    AUTH_FILE=auth.cfg python3 setup.py test

or::

    AUTH_FILE=auth.cfg pytest tests

where ``auth.cfg`` is the name of the configuration file.

To use already recorded cassettes simple omit the environment variable::

    python3 setup.py test

or::

    pytest tests


.. toctree::
    :maxdepth: 2

