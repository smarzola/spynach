from setuptools import setup, find_packages

version = '0.3'

setup(name='spynach',
      version=version,
      description="Simple and Lightweight WSGI Web Framework",
      long_description="""\
Spynach is a lightweight WSGI Python framework for rapid prototyping of web applications. Spynach has been developed
with a syntax similar to the one of the Turbogears2 framework to permit to develop fast and small web applications which
can be quickly switched to a full stack framework when necessary.
""",
      classifiers=["Development Status :: 4 - Beta",
                   "License :: OSI Approved :: GNU General Public License (GPL)",
                   "Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware",
                   "Programming Language :: Python",
                   "Topic :: Internet :: WWW/HTTP :: WSGI",
                   "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
                   "Topic :: Software Development :: Libraries :: Application Frameworks",
                   "Environment :: Web Environment",
                   "Intended Audience :: Developers"],
      keywords='wsgi web simple light',
      author='Simone Marzola',
      author_email='marzolasimone@gmail.com',
      url='http://simock85.github.com/spynach/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      data_files=[('', ['README.rst'])],
      zip_safe=False,
      install_requires=[
          'webob>1.2b4',
          'jinja2',
          'wtforms',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
