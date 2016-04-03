from __future__ import unicode_literals

import tg
from tg.decorators import before_validate

import os
import hashlib

ROOT = '/'
CSRF_TOKEN = '_csrf_token'
EXPIRES = 600  # seconds
ENCODING = 'latin1'


def _get_conf():
    """
    Return CSRF configuration options.

    This function raises ``KeyError`` if configuration misses
    """
    conf = tg.config
    csrf_secret = conf['csrf.secret']
    csrf_token_name = str(conf.get('csrf.token_name', CSRF_TOKEN))
    csrf_path = conf.get('csrf.path', ROOT).encode(ENCODING)
    try:
        cookie_expires = int(conf.get('csrf.expires', EXPIRES))
    except ValueError:
        cookie_expires = EXPIRES
    return csrf_secret, csrf_token_name, csrf_path, cookie_expires


def _generate_csrf_token():
    """
    Generate and set new CSRF token in cookie. The generated token is set to
    ``request.csrf_token`` attribute for easier access by other functions.
    """
    secret, token_name, path, expires = _get_conf()
    sha256 = hashlib.sha256()
    sha256.update(os.urandom(8))
    token = sha256.hexdigest().encode(ENCODING)
    tg.response.signed_cookie(token_name, token, secret,
                              path=path, max_age=expires)
    tg.request.csrf_token = token.decode(ENCODING)


@before_validate
def csrf_token(remainder, params):
    """
    Create and set CSRF token in preparation for subsequent POST request. This
    decorator is used to set the token. It also sets the ``'Cache-Control'``
    header in order to prevent caching of the page on which the token appears.

    When an existing token cookie is found, it is reused. The existing token is
    reset so that the expiration time is extended each time it is reused.

    The POST handler must use the :py:func:`~csrf_protect` decorator for the
    token to be used in any way.

    The token is available in the ``tg.request`` object as ``csrf_token``
    attribute::

        @csrf_token
        @expose('myapp.templates.put_token')
        def put_token_in_form():
            return dict(token=request.csrf_token)

    In a view, you can render this token as a hidden field inside the form. The
    hidden field must have a name ``_csrf_token``::

        <form method="POST">
            <input type="hidden" name="_csrf_token" value="{{ token }}">
            ....
        </form>
    """
    req = tg.request._current_obj()

    secret, token_name, path, expires = _get_conf()
    token = req.signed_cookie(token_name, secret=secret)
    if token:
        # We will reuse existing tokens
        tg.response.signed_cookie(token_name, token, secret,
                                  path=path, max_age=expires)
        req.csrf_token = token.decode('utf8')
    else:
        _generate_csrf_token()
    # Pages with CSRF tokens should not be cached
    req.headers[str('Cache-Control')] = ('no-cache, max-age=0, '
                                         'must-revalidate, no-store')


@before_validate
def csrf_protect(remainder, params):
    """
    Perform CSRF protection checks. Performs checks to determine if submitted
    form data matches the token in the cookie. It is assumed that the GET
    request handler successfully set the token for the request and that the
    form was instrumented with a CSRF token field. Use the
    :py:func:`~csrf_token` decorator to do this.

    Generally, the handler does not need to do anything
    CSRF-protection-specific. All it needs is the decorator::

        @csrf_protect
        @expose('myapp.templates.protected_post_handler')
        def protected_post_handler():
            if successful:
                tg.redirect('/someplace')
            return dict(errors="There were some errors")

    """
    req = tg.request._current_obj()

    secret, token_name, path, expires = _get_conf()
    token = req.signed_cookie(token_name, secret=secret)
    if not token:
        tg.abort(403, 'The form you submitted is invalid or has expired')

    form_token = req.args_params.get(token_name)
    if form_token != token.decode(ENCODING):
        tg.response.delete_cookie(token_name, path=path)
        tg.abort(403, 'The form you submitted is invalid or has expired')
