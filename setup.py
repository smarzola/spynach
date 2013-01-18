from setuptools import setup, find_packages
import sys, os

version = '0.4.2'

setup(name='artichoke',
      version=version,
      description="Simple and Lightweight WSGI Web Framework",
      long_description="""\
Artichoke is a lightweight WSGI Python framework for rapid prototyping of web applications. Artichoke has been developed with a syntax similar to the one of the Turbogears2 framework to permit to develop fast and small web applications which can be quickly switched to a full stack framework when necessary.
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
      author='AXANT',
      author_email='tech@axant.it',
      url='http://www.axantlabs.com/artichoke',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'webob',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
