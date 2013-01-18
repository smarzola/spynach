from webob import Request, Response
from webob.exc import HTTPException
from authenticator import CookieAuthenticator
from mail_traceback import send_traceback, format_traceback
import traceback, mimetypes, os
from controller import request as a_request, response as a_response

class ArtichokeHelpers(object):
    pass

class ArtichokeCore(object):
    def __init__(self, root, templates_path, config={}):
        self.minify_templates = config.get('templates.minify', False)
        self.statics = config.get('statics', 'public')
        self.autoreload_templates = config.get('autoreload', False)
        self.force_request_encoding = config.get('force_request_encoding', 'utf-8')
        
        requested_authenticator = config.get('authenticator')
        if not requested_authenticator:
            self.authenticator = CookieAuthenticator()
        else:
            self.authenticator = requested_authenticator()

        self.root = root(self, templates_path, config.get('helpers', ArtichokeHelpers()))

    def __call__(self, environ, start_response):
        request = Request(environ=environ)
        environ['artichoke.locals'].register(environ, a_request, request)

        response = Response(body="Artichoke Default Page", content_type='text/html', charset='utf-8')
        environ['artichoke.locals'].register(environ, a_response, response)

        if self.force_request_encoding:
            request.charset = self.force_request_encoding

        static_path = self.statics + request.path_info
        if os.path.exists(static_path) and os.path.isfile(static_path):
            response.body = open(static_path).read()
            response.status = 200
            response.content_type = mimetypes.guess_type(static_path)[0]
        else:
            try:
                self.authenticator.authenticate(request)
                self.root._dispatch(request)
                self.authenticator.inject_cookie(response)
            except HTTPException, e:
                response = e
                self.authenticator.inject_cookie(response)
        return response(environ, start_response)

class ErrorMiddleware(object):
    def __init__(self, app, core, config):
        self.app = app
        self.mail_errors_to = config.get('mail_errors_to')
        self.mail_errors_from = config.get('mail_errors_from', 'artichoke@localhost')
        self.traceback = config.get('traceback', True)
 
    def __call__(self, environ, start_response):
        try:
            return self.app(environ, start_response)
        except:
            resp = Response(body="Artichoke Error Middlware", content_type='text/html', charset='utf-8')

            if self.mail_errors_to:
                send_traceback(self.mail_errors_from, self.mail_errors_to)

            if self.traceback:
                format_error_body = traceback.format_exc()
                try:
                    format_error_body = format_traceback()
                    format_content_type = 'text/html'
                except Exception, e:
                    format_content_type = 'text/plain'
                resp.body = format_error_body
                resp.status = 500
                resp.content_type = format_content_type
            else:
                resp.body = "Internal Server Error"
                resp.status = 500

            return resp(environ, start_response)
            
class ThreadLocalsManager(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        try:
            environ['artichoke.locals'] = self
            environ['artichoke.registered_locals'] = []
            return self.app(environ, start_response)
        finally:
            for ri in environ['artichoke.registered_locals']:
                ri._pop_object()

    def register(self, environ, proxy, instance):
        environ['artichoke.registered_locals'].append(proxy)
        proxy._set_object(instance)

class Application(object):
    def __init__(self, root, templates_path, config={}):
        self.core = ArtichokeCore(root, templates_path, config)
        self.app = self.core

        for Middleware in config.get('middlewares', []):
            self.app = Middleware(self.app, self.core, config)

        self.app = ErrorMiddleware(self.app, self.core, config)
        self.app = ThreadLocalsManager(self.app)

    def __call__(self, environ, start_response):
        return self.app(environ, start_response)
