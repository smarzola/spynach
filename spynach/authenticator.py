#
class ArtichokeUser(object):
    def __init__(self, user_name, password):
        self.user_name = user_name
        self.password = password

class CookieAuthenticator(object):
    def __init__(self, cookie_name='artichoke_auth'):
        self.cookie_name = cookie_name

    def authenticate(self, request):
        request.identity = None

        auth_cookie = request.cookies.get(self.cookie_name)
        if auth_cookie:
            cookie_value = auth_cookie.decode('base64')
            login, password = cookie_value.split(':', 1)
            request.identity = {'user': ArtichokeUser(login, password)}

    def inject_cookie(self, response):
        skip_user = False

        try:
            artichoke_user = response.identity and response.identity['user']
        except:
            skip_user = True

        if not skip_user:
            if artichoke_user:
                cookie_value = u'%s:%s' % (artichoke_user.user_name, artichoke_user.password)
                cookie_value = cookie_value.encode('utf-8')
                cookie_value = cookie_value.encode('base64').rstrip()

                response.set_cookie(self.cookie_name, cookie_value, path='/')
            else:
                response.delete_cookie(self.cookie_name)



