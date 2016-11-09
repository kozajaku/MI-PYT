|Build Status| |Docbuild status|

twitterjk
=========

Welcome to the documentation of tool twitterjk. This tool was created for the purposes of MI-PYT lecture at
FIT CTU college.

The tool is simple program written in Python that is able to query tweets through Twitter API and show them
in readable format to the user in console or through simple web GUI.

Documentation
-------------

Documentation can be found online on `twitterjk.readthedocs.io <http://twitterjk.readthedocs.io/>`_ or
you can build it manually by clonning the repository and executing::

    cd docs
    python3 -m pip install -r requirements.txt
    make html

Documentation is now created in ``docs/_build/html/``.

You can also run the documentation doctest::

    make doctest

TestPyPi
--------

Module is also uploaded on `testPyPi <https://testpypi.python.org/pypi/twitterjk>`_.

.. |Build Status| image:: https://travis-ci.com/kozajaku/MI-PYT.svg?token=qexzosAyQM9jnGAQRNvZ&branch=master
    :target: https://travis-ci.com/kozajaku/MI-PYT
.. |Docbuild Status| image:: https://readthedocs.org/projects/twitterjk/badge/?version=latest
    :target: http://twitterjk.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status