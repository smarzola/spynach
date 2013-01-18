import artichoke, os, mimetypes, base64
from artichoke import request, response, expose, url, redirect, flash
from artichoke import FormBuilder

class SubController(artichoke.Controller):
    @expose()
    def about(self, args, params):
        return 'HELLO %s' % str(args)

    @expose()
    def index(self, args, params):
        return 'INDEX'

    @expose()
    def not_found(self, args, params):
        return 'Sub Not Found'

class RootController(artichoke.Controller):
    def __init__(self, application, templates_path, helpers):
        super(RootController, self).__init__(application, templates_path, helpers)
        self.sub = SubController(application, os.path.join(templates_path, 'sub'), helpers)

    @expose('index')
    def index(self, args, params):
        return dict(foo=False, form=FormBuilder('/echo_image', {'image':{'type':'file'}}))

    @expose()
    def echo_image(self, args, params):
        if params.has_key('image'):
            image = params['image']
            value = "data:%s;base64," % (mimetypes.guess_type(image.filename)[0] or "application/octet-stream")
            value += base64.b64encode(image.file.read())
        else:
            value = ''

        s = '''<html>
<head>
</head>
<body>
    <img src="%s"/>
</body>
</html>''' % value
        return s

    @expose('index')
    def other(self, args, params):
        foo = params.get('foo', False)
        flash('Flash here!')
        return dict(foo=foo)

    @expose()
    def crash(self, args, params):
        raise Exception('FATAL')

    def hidden(self, args, params):
        return 'HIDDEN'

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


app = artichoke.Application(root=RootController, templates_path='views')

if __name__ == '__main__':
    from artichoke.server import serve
    serve(app)
