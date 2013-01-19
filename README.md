## Welcome to Spynach.
Spynach is a lightweight WSGI Python framework for rapid prototyping of web applications built upon [Artichoke](https://bitbucket.org/axant/artichoke).
Spynach has been developed with a syntax similar to the one of the Turbogears2 framework
to permit to develop fast and small web applications which can be quickly switched to a full stack
framework when necessary. It includes ming (mongodb ODM) and Jinja2 template engine.

## How to install Spynach

You can install Spynach both from an official release trough setuptools or by fetching the development version from the repositories

### Installing stable version with setuptools

Spynach releases require Python and setuptools to be installed

### Python

Spicy-Artichoke works with any version of python between 2.5 and 2.7.

### Setuptools

To install setuptools by hand, first download [ez_setup.py](http://peak.telecommunity.com/dist/ez_setup.py) then invoke it using the Python interpreter into which you want to install setuptools.

    $ sudo python ez_setup.py

### Spynach

    $ sudo easy_install spynach

This should install the last stable release of spynach and download 
all the required dependencies including Jinja2, Paste, WebOb and Ming.

### Upgrading Spynach

    $ sudo easy_install -U spynach
