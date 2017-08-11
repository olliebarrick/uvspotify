import uvhttp.http

class Oauth(uvhttp.http.Session):
    """
    Oauth client for :mod:`uvhttp`.
    """

    def __init__(self, loop, auth_url, token_url, client_id, redirect_url=None, conn_limit=10):
        """
        * ``loop`` is the asyncio loop to use.
        * ``auth_url`` authorization url of the oauth endpoint (e.g., https://example.com/authorize).
        * ``token_url`` token url of the oauth endpoint (e.g., https://example.com/token).
        * ``client_id`` is the oauth client id.
        * ``callback_url`` is the URL of the callback in your web application.
        """
        pass

    def authenticate_url(self, *scopes):
        """
        Get the URL to redirect the Spotify user to. This URL should be loaded
        in the user's browser.
        """
        pass

    def is_registered(self, identifier):
        """
        Check if an identifier is already registered.
        """
        pass

    def register_auth_code(self, identifier, code):
        """
        Register the ``code`` from the oauth callback response with a unique
        identifier.
        """
        pass

    async def get_token(self, identifier):
        """
        Get an authentication token for an identifier. Return an access token
        that can be used in a cookie.
        """
        pass

    async def request(self, identifier, *args, **kwargs):
        """
        Make a request, but add the token for the given identifier to
        the headers to authenticate the request. See :class:`uvhttp.http.Session`.
        """
        pass
