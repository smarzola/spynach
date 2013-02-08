Welcome to Spynach!
=====================================

.. image:: https://travis-ci.org/simock85/spynach.png?branch=master
   :target: http://travis-ci.org/simock85/spynach

Spynach is a fast and lightweight WSGI Python framework for rapid prototyping of web applications, built upon
`Artichoke <http://bitbucket.org/axant/artichoke>`_.

Spynach has been developed with a syntax similar to the one of the Turbogears2 framework to permit to develop fast
and small web applications which can be quickly switched to a full stack framework when necessary.

Its main purpose is to work natively on the available Cloud Application Platforms, like Heroku, Red Hat OpenShift,
Google App Engine.

Spynach ships packed with a bunch of useful tools:

- Jinja2 template engine
- WTForms for forms validation and rendering

Since version 0.3 Spynach supports pluggables, the MongoDB native support has been dropped for native compatibility with
Google App Engine PaaS. MongoDB support is now provided by the spynach_ming plugin.

