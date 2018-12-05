import json
from jupyterhub.handlers import BaseHandler
from jupyterhub.auth import Authenticator
from jupyterhub.utils import url_path_join
from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado.escape import url_escape
from traitlets import Unicode
from urllib.parse import urlparse, urlunparse, urlencode
from urllib.request import urlopen


class GirderOAuthLoginHandler(BaseHandler):

    def _get_redirect(self):
        redirect_url = self.authenticator.jupyterhub_url
        redirect_url += '/hub/login?girderToken={girderToken}&next='
        redirect_url += self.get_argument('next', '')
        url = urlunparse(
            urlparse(self.authenticator.api_url + '/oauth/provider')._replace(
                query=urlencode({'redirect': redirect_url})
            )
        )
        with urlopen(url) as resp:
            providers = json.loads(resp.read().decode('utf-8'))
            return providers[self.authenticator.girder_provider]

    def _render(self, login_error=None, username=None):
        return self.render_template(
            'login.html',
            next=url_escape(self.get_argument('next', default='')),
            username=username,
            login_error=login_error,
            custom_html=self.authenticator.custom_html,
            login_url=self.settings['login_url'],
            authenticator_login_url=self._get_redirect()
        )

    @gen.coroutine
    def get(self):
        token = self.get_argument('girderToken', default=False)
        user = self.current_user
        if token and not user:
            username = None
            if token:
                me_url = '%s/user/me' % self.authenticator.api_url
                girder_token = token
                headers = {
                    'Girder-Token': girder_token
                }
                http_client = AsyncHTTPClient()
                r = yield http_client.fetch(me_url, headers=headers)
                if r.code == 200:
                    response_json = json.loads(r.body.decode('utf8'))
                    if response_json is not None:
                        username = response_json['login']
                        # potentially store 'girder_token'
                        user = self.user_from_username(username)

        if user:
            self.set_login_cookie(user)

            _url = url_path_join(self.hub.server.base_url, 'home')
            next_url = self.get_argument('next', default=False)
            if next_url:
                _url = next_url

            self.redirect(_url)
        else:
            self.finish(self._render())


class GirderOAuthAuthenticator(Authenticator):
    """Accept a girderToken via query parameter."""

    login_service = Unicode(
        'GirderOAuth',
        config=False
    )

    jupyterhub_url = Unicode(
        help='The url to the JupyterHub instance',
        default_value='https://jupyterhub.local.wholetale.org',
        config=True
    )

    api_url = Unicode(
        help='The url to the girder server to use for token validation',
        default_value='https://girder.dev.wholetale.org/api/v1',
        config=True
    )

    girder_provider = Unicode(
        help='Girder OAuth Provider',
        default_value='Globus',
        config=True
    )

    def get_handlers(self, app):
        return [
            (r'/login', GirderOAuthLoginHandler),
        ]

    @gen.coroutine
    def authenticate(self, *args):
        raise NotImplementedError()
