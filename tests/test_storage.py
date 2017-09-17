# -*- coding: utf-8 -*-
from os import path
from tempfile import mkdtemp

from tg import expose, TGController, AppConfig
from webtest import TestApp, Upload

import tgext
from tgext.utils.storage import store


TESTS_DIR = path.abspath(path.join(path.dirname(__file__), '..', 'tests'))
PATH_TO_FILE = path.join(TESTS_DIR, 'stuff', 'tg.png')
PATH_TO_STORAGE = mkdtemp()


class RootController(TGController):
    @expose()
    def post_form(self, **kwargs):
        stored_filename = store(kwargs.get('file'))
        return stored_filename

    @expose()
    def form(self):
        return '''
        <form method="POST" action="/post_form">
            <input type="file" name="file">
        </form>'''


class TestStorageManager(object):
    @classmethod
    def setup_class(cls):
        config = AppConfig(minimal=True, root_controller=RootController())
        config.paths['static_files'] = PATH_TO_STORAGE
        cls.wsgi_app = config.make_wsgi_app()

    def make_app(self, **options):
        return TestApp(self.wsgi_app)

    def test_file_is_stored(self):
        app = self.make_app()
        form = app.get('/form').forms[0]

        form['file'] = Upload(PATH_TO_FILE)

        stored_filename = form.submit().text
        stored_file_path = path.join(PATH_TO_STORAGE, stored_filename)

        file_checksum = self.md5(PATH_TO_FILE)
        stored_file_checksum = self.md5(stored_file_path)

        assert file_checksum == stored_file_checksum

    @classmethod
    def teardown_class(cls):
        import shutil
        shutil.rmtree(PATH_TO_STORAGE)

    def md5(self, fname):
        import hashlib
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
