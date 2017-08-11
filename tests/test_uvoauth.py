from nose.tools import *
from uvhttp.utils import start_loop
from uvoauth.uvoauth import Oauth
from sanic import Sanic
from sanic.response import json
import functools
import urllib.parse

def oauth_server(func):
    @functools.wraps(func)
    @start_loop
    async def oauth_wrapper(loop, *args, **kwargs):
        app = Sanic(__name__)

        @app.route('/authorize')
        async def authorize(request):
            return {
                ""
            }

        @app.route('/token')
        async def token(request):
            pass

        @app.route('/api')
        async def api(request):
            pass

        server = await app.create_server(host='127.0.0.1', port=8089)

        try:
            await func(app, loop, *args, **kwargs)
        finally:
            server.close()

    return oauth_wrapper

@oauth_server
async def test_uvoauth(app, loop):
    url = 'http://127.0.0.1:8089/'

    oauth = Oauth(loop, url + 'authorize', url + 'token', '1234',
            'http://example.com/callback')

    auth_url = oauth.authenticate_url('scope1', 'scope2')
    auth_url = urllib.parse.urlsplit(auth_url)
    qs = urllib.parse.parse_qs(auth_url.query)

    assert_equal(qs['client_id'], '1234')
    assert_equal(qs['response_type'], 'code')
    assert_equal(qs['redirect_uri'], 'http://example.com/callback')
    assert_equal(qs['scope'], 'scope1 scope2')

    assert_equal(oauth.is_registered('newuser'), False)

    oauth.register_auth_code('newuser', 'abcdefgh')

    assert_equal(oauth.is_registered('newuser'), True)

    assert_equal(await oauth.get_token('newuser'), 'hello')

    response = await oauth.request('newuser', b'GET', url + 'api')
    assert_equal(response.json(), {'authorization': 'Bearer hello'})
