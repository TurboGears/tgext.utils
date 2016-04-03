# -*- coding: utf-8 -*-
from tg import expose, TGController, AppConfig, request
from webtest import TestApp
from tgext.utils.csrf import csrf_protect, csrf_token


class RootController(TGController):
    @csrf_token
    @expose()
    def index(self):
        return 'Hello World'

    @csrf_protect
    @expose()
    def post_form(self, **kwargs):
        return 'OK!'

    @csrf_token
    @expose()
    def form(self):
        return '''
        <form method="POST" action="/post_form">
            <input type="hidden" name="_csrf_token" value="%s">
        </form>''' % request.csrf_token


class TestWSGIMiddleware(object):
    @classmethod
    def setup_class(cls):
        config = AppConfig(minimal=True, root_controller=RootController())
        config['csrf.secret'] = 'MYSECRET'
        cls.wsgi_app = config.make_wsgi_app()

    def make_app(self, **options):
        return TestApp(self.wsgi_app)

    def test_token_is_set(self):
        app = self.make_app()
        app.get('/index')
        assert '_csrf_token' in app.cookies

    def test_token_is_validated(self):
        app = self.make_app()
        resp = app.get('/post_form', status=403)
        assert 'The form you submitted is invalid or has expired' in resp

    def test_cookie_alone_is_not_enough(self):
        app = self.make_app()
        app.get('/index')
        resp = app.get('/post_form', status=403)
        assert 'The form you submitted is invalid or has expired' in resp

    def test_cookie_and_form_pass_check(self):
        app = self.make_app()
        resp = app.get('/form')
        resp = resp.forms[0].submit()
        assert 'OK' in resp