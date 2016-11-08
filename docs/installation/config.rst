Configuration file
==================

Nowadays, it is not possible to access Twitter API without being authorized. In order to be able to use the **twitterjk**
tool, you must first create a configuration file containing information about logging into your Twitter account. To do so
you must follow the following steps:

- Create an account on `Twitter <https://twitter.com/>`_ (skip this step if you already have one)
- Navigate to `apps.twitter.com <https://apps.twitter.com/>`_ in your web browser
- Log into your Twitter account if you have not done this yet
- Click on *Create New App*
- Choose some *Name*, *Description* and *Website* for your new app
- Read the *Twitter Developer Agreement* and check that you agree
- Click on *Create your Twitter application*
- Choose your newly created application
- In the top panel click on *Keys and Access Tokens*
- Copy out *Consumer key (API Key)* and *Consumer Secret (API Secret)* parameters

Now you have API key and API secret that must be pasted into configuration file. Create new text file named
``auth.cfg`` with the following layout::

    [twitter]
    key = yourAPIkey
    secret = yourAPIsecret

Of course, replace ``yourAPIkey`` by your real API key and ``yourAPIsecret`` by your real API secret.

Location
--------

**twitterjk** tool implicitly looks for configuration file named ``auth.cfg`` in the same directory where the tool start
was initiated, however, you can rename it and put it wherever you want and then point to it by using console argument
``--config``.