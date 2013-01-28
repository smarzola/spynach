from webob import Request, Response
from webob.exc import HTTPFound
import inspect, pickle, base64, types, urllib
from thread_locals import ThreadLocalProxy
from template import SpynachTemplateLoader
try:
    import json
except ImportError:
    import simplejson as json

request = ThreadLocalProxy()
response = ThreadLocalProxy()

def expose(template = None,
           content_type = 'text/html'):

    if template == 'json':
        content_type = 'application/json'
        template = None

    def decorate(f):
        f.exposed = True

        if not hasattr(f, 'spynach'):
            f.spynach = {}

        f.spynach['template'] = template
        f.spynach['content-type'] = content_type
        return f
    return decorate

def url(base_url, params={}):
    if base_url.startswith('/'):
        base_url = request.environ['SCRIPT_NAME'] + base_url

    if params:
        sane_params = {}
        for key in params.iterkeys():
            sane_params[key] = params[key].encode('utf-8')
        return '?'.join((base_url, urllib.urlencode(sane_params)))

    return base_url


def redirect(where):
    exc = HTTPFound(location=where)
    try:
        exc.identity = response.identity
    except:
        pass

    if response.flash_obj:
        decoded_flash = pickle.dumps(response.flash_obj)
        exc.set_cookie('flash_obj', base64.b64encode(decoded_flash))

    raise exc

def flash(msg, css_class='warning'):
    response.flash_obj = {'msg':msg, 'class':css_class}

class Controller(object):
    def __init__(self, application, template_path, helpers):
        self.template_path = template_path
        self.application = application
        self.loader = SpynachTemplateLoader(template_path, self.application.autoreload_templates)
        self.helpers = helpers
        self.templates = {}

    def render(self, template, params):
        tmpl = self.loader.load(template)
        return tmpl.render(params)

    @expose()
    def not_found(self, args, params):
        response.content_type = 'text/html'
        response.status = 404
        return '''
<html>
   <head>
       <title>Page not Found</title>
   </head>
   <body>
       <h1>Page Not Found</h1>
       <div style="font-size:small">spynach Framework</div>
   </body>
</html>
'''

    def _dispatch(self, request):
        path = request.path_info.split('/')
        while path and not path[0]:
            path.pop(0)

        if not path:
            path = ['index']

        members = dict(inspect.getmembers(self))
        call = self

        if isinstance(call, Controller):
            while path[0:]:
                subpath = path[0]
                members = dict(inspect.getmembers(call))
                try:
                    call_candidate = members[subpath]
                    if isinstance(call_candidate, Controller) or\
                       (hasattr(call_candidate, 'exposed') and call_candidate.exposed):
                        call = call_candidate
                        path = path[1:]
                    else:
                        break
                except:
                    break

        if isinstance(call, Controller):
            if path:
                call = call.not_found
            else:
                call = call.index

        self.do_call(call, request, path[:])

    def do_call(self, call, request, path):
        response.content_type = call.spynach['content-type']
        self.inject_tools(request, response)

        if call.spynach['template']:
            tmpl_context = {}
            tmpl_context['a'] = type('Bunch', (object,), {'url':staticmethod(url)})
            tmpl_context['h'] = self.helpers
            tmpl_context['request'] = request
            tmpl_context['response'] = response
            tmpl_context.update(call(path, request.params))

            template = call.spynach['template']
            response.body = self.render(template, tmpl_context)
        elif call.spynach['content-type'] == 'application/json':
            response.body = json.dumps(call(path, request.params))
        else:
            response.body = call(path, request.params)

        return response

    def inject_tools(self, request, response):
        response.flash_obj = {}
        if request.cookies.get('flash_obj'):
            try:
                decoded_flash = request.cookies['flash_obj'].decode('base64')
                response.flash_obj = pickle.loads(decoded_flash)
            except Exception, e:
                pass
            response.delete_cookie('flash_obj')
