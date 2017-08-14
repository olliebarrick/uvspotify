from sanic.response import json
from uvhttp.utils import http_server, HttpServer
from uvspotify.uvspotify import Spotify, SpotifyScopes
from nose.tools import *
import argparse
import asyncio
import ssl
import urllib.parse

class CallbackServer(HttpServer):
    def add_routes(self):
        super().add_routes()
        self.app.add_route(self.callback, '/callback')

    async def callback(self, request):
        self.spotify.register_auth_code('user', request.args['code'][0])
        self.registered.set()
        return json({})

@http_server(CallbackServer)
async def main(server, loop):
    parser = argparse.ArgumentParser()
    parser.add_argument('client_id', help='Client id from Spotify.')
    parser.add_argument('client_secret', help='Client id from Spotify.')
    parser.add_argument('callback', help='Callback address that your server will be reachable on (e.g., https://example.com/, excluding /callback).')
    args = parser.parse_args()

    server.registered = asyncio.Event(loop=loop)

    ctx = ssl.create_default_context()
    spotify = Spotify(loop, args.client_id, args.client_secret,
                      args.callback + 'callback', ssl=ctx)
    server.spotify = spotify

    print(spotify.authenticate_url(SpotifyScopes.USER_READ_PLAYBACK_STATE))

    await server.registered.wait()

    response = await spotify.api(b'GET', b'/me/player/devices',
                                 identifier='user', ssl=ctx)
    assert_equal(response.status_code, 200)
    for device in response.json()['devices']:
        print(device['name'])

if __name__ == '__main__':
    main()
