Quickstarting with artichoke
==============================

Creating a spicy-artichoke application
------------------------------------

Artichoke applications can be created from the `artichoke.application.Application` by
passing a root `artichoke.controller.Controller` and a path where to find the templates
exposed by the controller methods.

You can serve your application both using `mod_wsgi <http://www.modwsgi.org>`_ or by using the internal
artichoke wsgi server. The internal server will also reload application if any file of the application
itself is changed, this comes at a high performance cost so it is only intended for development
and not for production deploy.

.. code-block:: python

    import artichoke
    from artichoke.server import serve

    app = artichoke.Application(root=RootController, templates_path='views')

    if __name__ == '__main__':
        serve(app)

Creating a controller for your application
-------------------------------------------------

Each artichoke application requires a root controller which will serve requests sent
to the application itself. The root controller can have any number of sub controllers
as instance variables to serve nested urls.

.. code-block:: python

    import artichoke
    from artichoke import expose
    from artichoke.server import serve

    class RootController(artichoke.Controller):
        @expose(content_type='text/plain')
        def index(self, args, params):
            return 'Hi from my first artichoke application'

        @expose()
        def hello(self, args, params):
            return '<html><head></head><body>Hello World</body></html>'

    serve(artichoke.Application(root=RootController, templates_path='views'))



Each method exposed with the *@expose* decorator will be served as an url inside the root
of the application. In this case */hello* will be served by the hello method which doesn't
expose any template and so it returns the html to be served as a string with the default
content type (which is text/html).

An exception to this rule are the *index* and *not_found* methods.
The first will be served with the last part of the url is the controller itself (for example
the *index* of your root controller will serve the */* url).
While the *not_found* one is called when no method or subcontroller has been found to serve
the requested url. This method by default returns a 404 with a standard html but can be
overridden by the user.

Apart from exposed methods the controllers will inherit some utility methods.
Those include:

 * **render(self, template, params)**  *which will render the given template file (requires extension) from the template_path* 


Serving Templates
--------------------

Being able to serve content isn't really useful if you can serve only strings.
For this reason the expose decorator supports declaring both a content_type and
a template. The first will be useful when you need to serve JSON or files and the
latter will be used frequently to serve web pages.

Controller Example
~~~~~~~~~~~~~~~~~~~~~

When exposing a template your method should return a dict.
Each entry inside the dict will be exposed as a variable inside the template

.. code-block:: python

    import artichoke
    from artichoke import request, response, expose, redirect, url, flash
    from artichoke.server import serve

    class RootController(artichoke.Controller):
        @expose('index')
        def index(self, args, params):
            who = params.get('who', 'World')
            return dict(who=who)

    serve(artichoke.Application(root=RootController, templates_path='views'))

View Example
~~~~~~~~~~~~~~~~~~~~

Save the following code as **index.choke** inside the *views* directory (the one
passed to the Application as **templates_path** argument) and it will be
served when calling the */index* url as the *@expose* decorator declared
that the index method should serve the index template.

.. code-block:: html

    <html>
        <head>
            <title>Hello ${who}</title>
        </head>

        <body>
            Welcome ${who}
        </body>
    </html> 

Serving Nested Urls
----------------------

Is it possible to create controllers inside controllers, this will permit to
serve nested urls. To perform this just allocate more controllers inside the
**__init__** of the root controller. Each controller will serve the url equal
to the name of the variable it has been assigned to.

In the following example we the **/sub/hello** url will be served by the *hello*
method of the *SubController* class as it has been created inside the RootController.

.. code-block:: python

    import artichoke
    from artichoke import request, response, expose, redirect, url, flash
    from artichoke.server import serve

    class SubController(artichoke.Controller):
        @expose()
        def hello(self, args, params):
            return 'Hello World'

    class RootController(artichoke.Controller):
        def __init__(self, templates_path, helpers):
            super(RootController, self).__init__(templates_path, helpers)
            self.sub = SubController(os.path.join(templates_path, 'sub'), helpers)

        @expose('index')
        def index(self, args, params):
            who = params.get('who', 'World')
            return dict(who=who)

    serve(artichoke.Application(root=RootController, templates_path='views'))

Utility Functions
=========================

Artichoke Exposes a set of functions to help you create your application:

 * **redirect(where)** which will redirect the user to another url

 * **url(path, params=dict)** which will generate an url with the given parameters

 * **flash('message', 'class')**  will inject inside the response object of the 
    current call (or next call after a redirect) 
    the **flash_obj** dictionary which will expose the *msg* and *class* keys specified
    inside the *response.flash* call.

    As both the request and response objects are available inside the template context
    you can display the flash message inside the template with something like:

.. code-block:: html

    ${%if response.flash_obj:}
        <div>
            <div class="${response.flash_obj['class']}">${response.flash_obj['msg']}</div>
        </div>
    ${%end}


The Request and Response objects
==================================

``artichoke.request`` and ``artichoke.response`` objects are automatically
created by artichoke itself for each request.
For documentation about the request and response objects you can refer to
the `WebOb <http://pythonpaste.org/webob>`_ documentation.

The not_found method
========================

not_found method of a controller will be called when each other url resolution
method has failed to find a valid callable.

The default implementation of the method will set the *response.status* to **404**,
*response.headers['Content-Type']* to **text/html** and will return a simple error
message as an html page.

You can override this method to serve a different error page, 
implement different dispatching mechanisms or rest urls.
