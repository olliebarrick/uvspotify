from nose.tools import *
from uvhttp.utils import http_server
from uvhttp.dns import Resolver
from uvspotify.uvspotify import Spotify, SpotifyScopes
from uvspotify.utils import SpotifyServer
from uvoauth.utils import ACCESS_CODE
import ssl
import urllib.parse

@http_server(SpotifyServer)
async def test_spotify(server, loop):
    resolver = Resolver(loop)
    resolver.add_to_cache(b'accounts.spotify.com', 443,
            server.https_host.encode(), 60, port=server.https_port)
    resolver.add_to_cache(b'api.spotify.com', 443,
            server.https_host.encode(), 60, port=server.https_port)

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    spotify = Spotify(loop, '1234', '5678', 'http://example.com/callback',
            resolver=resolver, ssl=ctx)

    auth_url = spotify.authenticate_url(SpotifyScopes.USER_READ_PLAYBACK_STATE)
    auth_url = urllib.parse.urlsplit(auth_url)
    qs = urllib.parse.parse_qs(auth_url.query)

    assert_equal(auth_url.scheme, 'https')
    assert_equal(auth_url.netloc, 'accounts.spotify.com')
    assert_equal(auth_url.path, '/authorize')
    assert_equal(qs['scope'][0], SpotifyScopes.USER_READ_PLAYBACK_STATE)
    assert_equal(qs['redirect_uri'][0], 'http://example.com/callback')

    spotify.register_auth_code('newuser', ACCESS_CODE)

    response = await spotify.api(b'GET', b'/me/player/devices',
                                 identifier='newuser', ssl=ctx)

    assert_equal(response.json()['devices'][0]['name'], 'Kitchen')
    assert_equal(response.json()['devices'][1]['name'], 'Living Room')
