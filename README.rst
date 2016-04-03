About tgext.utils
=================

.. image:: https://travis-ci.org/amol-/tgext.utils.png?branch=master
    :target: https://travis-ci.org/amol-/tgext.utils

.. image:: https://coveralls.io/repos/amol-/tgext.utils/badge.png?branch=master
    :target: https://coveralls.io/r/amol-/tgext.utils?branch=master

.. image:: https://img.shields.io/pypi/v/tgext.utils.svg
   :target: https://pypi.python.org/pypi/tgext.utils

.. image:: https://img.shields.io/pypi/dm/tgext.utils.svg
   :target: https://pypi.python.org/pypi/tgext.utils

tgext.utils is a collection of utilities for the TurboGears2 web framework.

Installing
----------

tgext.utils can be installed from pypi::

    pip install tgext.utils

should just work for most of the users.

CSRF Protection
===============

``tgext.utils.csrf`` provides two decorators ``@csrf_token`` and ``@csrf_protect`` which
generate a CSRF token for inclusion in a form and check that the token is valid.

The user must apply ``@csrf_token`` decorator to the action that exposes the form,
and put an ``<input type="hidden">`` into the form with a ``request.csrf_token`` as
the value and ``_csrf_token`` as name:

.. code-block:: python

    @csrf_token
    @expose()
    def form(self):
        return '''
        <form method="POST" action="/post_form">
            <input type="hidden" name="_csrf_token" value="%s">
        </form>''' % request.csrf_token

The action that receives the form must have ``@csrf_protect`` decorator,
no particular action or check is required on this action:

.. code-block:: python

    @csrf_protect
    @expose()
    def post_form(self, **kwargs):
        return 'OK!'

