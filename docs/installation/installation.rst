Installation
============

When you have properly downloaded **twitterjk** source codes, you can now proceed with installation. You can use
already created ``setup.py`` file to make this really simple. Before installation, I really recommend to setup new Python
virtual environment if you have not done this yet. You can find information about how to do in :doc:`virtualenv`.

First navigate to the root directory of the **twitterjk** tool. ``setup.py`` file should be in this directory too. Now
you can invoke installation process by calling::

    python3 setup.py install

Note that before using the tool you have to create configuration file ``auth.cfg``. See :doc:`config`.

Installation from testPyPi
--------------------------

If you only want to try the **twitterjk** tool without the necessity to manually download source files, you can invoke::

    python3 -m pip install --extra-index-url https://testpypi.python.org/pypi twitterjk

Now you can use the tool in the same way as with manually downloaded source codes, however you will not be able to
run tests or generate documentation. Note that in this case you also have to create configuration file ``auth.cfg`` first
before executing the **twitterjk** tool. See :doc:`config`.
