How to install Artichoke
===========================

You can install artichoke both from an official release trough setuptools or by fetching the development version from the repositories

Installing stable version with setuptools
-------------------------------------------

Artichoke releases require Python and setuptools to be installed

Python
~~~~~~~~

Artichoke works with any version of python between 2.5 and 2.7. 
The most widely deployed version of python at the moment of this writing is version 2.5.

Setuptools
~~~~~~~~~~~~

.. code-block:: bash

    $ wget http://peak.telecommunity.com/dist/ez_setup.py | sudo python

You may also use your system's package for setuptools.

Artichoke
~~~~~~~~~~~~

.. code-block:: bash

    $ sudo easy_install artichoke

This should install the last stable release of artichoke and download 
all the required dependencies including Genshi, Paste and WebOb.

Upgrading Artichoke
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ sudo easy_install -U artichoke

