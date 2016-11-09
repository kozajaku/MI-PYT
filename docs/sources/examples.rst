Examples
========

Link creation
-------------

Function ``create_link`` can be very easily used to create new HTML link from
passed test and href. It can also use optional parameter as_search to prefix href
with ``/search?q=`` which can be afterwards easily used to create links
from webpage pointing to the same search page. Note that href parameter is
url escaped when as_search parameter is True.

.. testsetup::

    from twitterjk.twitter import create_link

.. doctest::

    >>> create_link("foo", "bar")
    '<a href="foo">bar</a>'
    >>> create_link("@foo", "@bar")
    '<a href="@foo">@bar</a>'
    >>> create_link("@python", "#test", True)
    '<a href="/search?q=%40python">#test</a>'
    >>> create_link("#wikileaks", "wikileaks", True)
    '<a href="/search?q=%23wikileaks">wikileaks</a>'

Create image
------------

Function ``create_image`` serves as a simple function for creating HTML image tags.
It has optional size parameter, where the size of Twitter image can be specified.

.. testsetup::

    from twitterjk.twitter import create_image

.. doctest::

    >>> create_image("http://foobar.com/img.jpeg")
    '<image src="http://foobar.com/img.jpeg" />'
    >>> create_image("http://foobar.com/img2.jpeg", "small")
    '<image src="http://foobar.com/img2.jpeg:small" />'

Tweet text enrichment
---------------------

Function ``text_with_entities`` is very powerful function that takes text
from passed tweet and enrich every entity inside with HTML links. For example,
every hashtag is replaced for exactly same text bounded by HTML tag pointing to the
search of the hashtag on the **twitterjk** page.

.. testsetup::

    from twitterjk.twitter import text_with_entities
    import json

Url entities
::::::::::::

Input tweet example:

.. testcode::

    url_tweet = json.loads('''
    {
      "text": "Today, Twitter is updating embedded Tweets to enable a richer photo experience: https:\/\/t.co\/XdXRudPXH5",
      "entities": {
        "hashtags": [],
        "symbols": [],
        "urls": [{
          "url": "https:\/\/t.co\/XdXRudPXH5",
          "expanded_url": "https:\/\/blog.twitter.com\/2013\/rich-photo-experience-now-in-embedded-tweets-3",
          "display_url": "blog.twitter.com\/2013\/rich-phot\u2026",
          "indices": [80, 103]
        }],
        "user_mentions": []
      }
    }''')
    result = text_with_entities(url_tweet)
    print(result)


Output text:

.. testoutput::

    Today, Twitter is updating embedded Tweets to enable a richer photo experience: <a href="https://blog.twitter.com/2013/rich-photo-experience-now-in-embedded-tweets-3">https://t.co/XdXRudPXH5</a>

User mention entities
:::::::::::::::::::::

Input tweet example:

.. testcode::

    user_mention_tweet = json.loads('''
    {
      "text": "We\u2019re excited to work closely with the external technical community and continue @twittereng\u2019s work with open source. cc @TwitterOSS",
      "entities": {
        "hashtags": [],
        "symbols": [],
        "urls": [],
        "user_mentions": [{
          "screen_name": "TwitterEng",
          "name": "Twitter Engineering",
          "id": 6844292,
          "id_str": "6844292",
          "indices": [81, 92]
        }, {
          "screen_name": "TwitterOSS",
          "name": "Twitter Open Source",
          "id": 376825877,
          "id_str": "376825877",
          "indices": [121, 132]
        }]
      }
    }''')
    result = text_with_entities(user_mention_tweet)
    print(result)


Output text:

.. testoutput::

    We’re excited to work closely with the external technical community and continue <a href="/search?q=%40twittereng">@twittereng</a>’s work with open source. cc <a href="/search?q=%40TwitterOSS">@TwitterOSS</a>

Hashtag entities
::::::::::::::::

Input tweet example:

.. testcode::

    hashtag_tweet = json.loads('''
    {
      "text": "Loved #devnestSF",
      "entities": {
        "hashtags": [{
          "text": "devnestSF",
          "indices": [6, 16]
        }],
        "symbols": [],
        "urls": [],
        "user_mentions": []
      }
    }''')
    result = text_with_entities(hashtag_tweet)
    print(result)


Output text:

.. testoutput::

    Loved <a href="/search?q=%23devnestSF">#devnestSF</a>


Symbol entities
::::::::::::::::

Input tweet example:

.. testcode::

    symbol_tweet = json.loads('''
    {
      "text": "$PEP or $COKE?",
      "entities": {
        "hashtags": [],
        "symbols": [
          {
            "text": "PEP",
            "indices": [
              0,
              4
            ]
          },
          {
            "text": "COKE",
            "indices": [
              8,
              13
            ]
          }
        ],
        "urls": [],
        "user_mentions": []
      }
    }''')
    result = text_with_entities(symbol_tweet)
    print(result)


Output text:

.. testoutput::

    <a href="/search?q=%24PEP">$PEP</a> or <a href="/search?q=%24COKE">$COKE</a>?


