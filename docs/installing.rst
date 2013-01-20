How to install Spynach
===========================

You can install spicy-artichoke both from an official release trough setuptools or by fetching the development version
from the repositories

Installing stable version with setuptools
-------------------------------------------

Spynach releases require Python and setuptools to be installed

Python
---------

Spynach works with any version of python between 2.5 and 2.7.

Setuptools
------------

To install setuptools by hand, first download ez_setup.py then invoke it using the Python interpreter into which
you want to install setuptools.

.. code-block:: bash

    $ sudo python ez_setup.py


Virtualenv
------------

Once you’ve got setuptools or distribute installed, you should install the virtualenv package.
To install the virtualenv package into your setuptools-enabled Python interpreter, use the easy_install command.

.. code-block:: bash

    $ sudo easy_install virtualenv


Spynach
-----------

Create a virtualenv and install spynach

.. code-block:: bash

    $ cd yourappfolder
    $ virtualenv --no-site-packages env
    $ source env/bin/activate
    (env)$ easy_install spynach

This should install the last stable release of spynach and download all the required dependencies including
Jinja2, Paste, WebOb, Ming and WTForms.

Upgrading Spynach
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    (env)$ easy_install -U spynach

