Advanced topics
===================

This section will cover some advanced functions of Spicy-spynach like helpers, authentication and form builder

Exposing Helpers inside templates
-----------------------------------

By default when you render a template from spynach **response**, **request** and the **h** variables
will be available inside the template. The last one will expose a collection of helpers useful while
creating templates.

By default this collection is empty, but you can override it by passing a different object to the
**config** parameter of the spynach *Application*

.. code-block:: python 

    from datetime import datetime
    import spynach
    from spynach.server import serve

    class AppHelpers(object):
        def copyright(self):
            return 'Copyright 2010-%s' % datetime.now().strftime('%Y')

    class RootController(spynach.Controller):
        @expose('index')
        def index(self, args, params):
            return dict()

    serve(spynach.Application(root=RootController, templates_path='views'))

.. code-block:: html

   <html>
        <head>
            <title>Hello World</title>
        </head>

        <body>
            Welcome, this page is ${h.copyright()} MySelf
        </body>
    </html> 

It might be useful inside your application to use `WebHelpers <http://webhelpers.groovie.org>`_ to implement
your helpers.

Authentication
------------------

By default the spynach framework will enable a simple authentication layer which will make possible
to login users by saving session cookies inside their browsers.

You will have just to implement your **/login** and **/logout** methods to save and delete the credentials
and permit to your users to login and logout

You can login an user by saving inside the **response.identity** variable a dictionary containing the
**user** key pointing to an object exposing at least a **user_name** and **password** properties.

When the user comes back the *response.identity* object will contain the data of the user that came back.
You can then logout the user by setting response.identity to **None**

.. code-block:: python

    from spynach import redirect, response, flash

    @expose()
    def login(self, args, params):
        class FakeUser(object):
            pass

        user = FakeUser()
        user.user_name = params['user']
        user.password = params['password']

        response.identity = {'user':user}
        flash('Welcome back!')
        return redirect('/index')

    @expose()
    def logout(self, args, params):
        response.identity = None
        return redirect('/index')


Form Builder
----------------

The **spynach.forms.FormBuilder** class permits to quickly create forms inside your web pages.

The first parameter of the constructor is the url where to submit the form data, the second parameter
is a dictionary with the field to expose inside the form and the third and optional one is the order
of the fields inside the form (omitting it will cause random order).

Each entry inside the fields dict will need a key with the same name of the parameter and a value
which must be a dictionary itself. The dictionary value can specify a label and a type for the field
(valid types are *textarea*, *password*, *text*, *file*). If nothing is specified it will default
to a text field with a label equal to the field key capitalized.

.. code-block:: python

        new_project_form = FormBuilder('/add_project', dict(name={},
                                                            download_url={},
                                                            short_desc={'label':'Short Description:'},
                                                            long_desc={'label':'Long Description:',
                                                                       'type':'textarea'},
                                                            icon={'type':'file'}),
                                       fields_order=['name', 'download_url', 'icon', 'short_desc',
                                                     'long_desc'])


To display the form inside the template you must pass the form to the template and call the **form.render()** method

Custom Middlewares
----------------------

Since version 0.3.1 spynach supports middlewares.
Registering middlewares is quite simple, just passing a list of middleware to create
to the ``middlewares`` configuration variable is enough.

Each middleware will receive the current application:``app``, spynach core:``core``
and configuration options:``config`` at construction

You can for example create a middleware that handles database models with sqlalchemy:

.. code-block:: python

    import sqlalchemy as sqla
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import scoped_session, sessionmaker

    DeclarativeBase = declarative_base()
    metadata = DeclarativeBase.metadata
    maker = sessionmaker(autoflush=True, autocommit=False)
    DBSession = scoped_session(maker)

    class SQLAMiddleware(object):
        def __init__(self, app, core, config):
            self.app = app

            self.engine = sqla.create_engine(config.get('sqlalchemy.url'), echo=False)
            self.session = config.get('sqlalchemy.session')

            metadata.create_all(self.engine)
            self.session.configure(bind=self.engine)

        def __call__(self, environ, start_response):
            self.session.begin()
            try:
                ans = self.app(environ, start_response)
                self.session.flush()
                self.session.commit()
            except:
                self.session.rollback()
                raise
            return ans

    app = spynach.Application(root=RootController, templates_path='views', 
                                config={'sqlalchemy.url':'sqlite:///devdata.db',
                                        'sqlalchemy.session':DBSession,
                                        'middlewares':[SQLAMiddleware]})



Application Configuration
----------------------------

Apart from the *root* and *templates_path* parameters the **Application** class constructor
accepts a thir parameter called **config**. 
This parameter contains a dictionary with various configuration options about the application itself:

 * **helpers** (*default: an empty object*) The application helpers object

 * **statics** (*default: 'public'*) The application static files path (will be available inside a controller as self.application.statics)

 * **middlewares** (*default: []*) List of middlewares to allocate around the application

 * **autoreload** (*default: False*) The application should disable the templates cache reloading them at each request

 * **authenticator** (*default: CookieAuthenticator*) The authenticator class to be used to authenticate users

 * **mail_errors_to** (*default: None*) Mail crash tracebacks to the specified address

 * **mail_errors_from** (*default: 'spynach@localhost'*) The *From* field of mailed tracebacks

 * **traceback** (*default: False*) On crash print traceback inside the web browser (you should disable this on production)
