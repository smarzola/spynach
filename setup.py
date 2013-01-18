from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='spicy-artichoke',
      version=version,
      description="Simple and Lightweight WSGI Web Framework",
      long_description="""\
Spycy-Artichoke is a lightweight WSGI Python framework for rapid prototyping of web applications. Spycy-Artichoke has been developed with a syntax similar to the one of the Turbogears2 framework to permit to develop fast and small web applications which can be quickly switched to a full stack framework when necessary.
""",
      classifiers=["Development Status :: 5 - Production/Stable",
                   "License :: OSI Approved :: GNU General Public License (GPL)",
                   "Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware",
                   "Programming Language :: Python",
                   "Topic :: Internet :: WWW/HTTP :: WSGI",
                   "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
                   "Topic :: Software Development :: Libraries :: Application Frameworks",
                   "Environment :: Web Environment"],
      keywords='wsgi web simple light',
      author='Simone Marzola',
      author_email='marzolasimone@gmail.com',
      url='http://www.axantlabs.com/artichoke',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'webob',
          'jinja2',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
