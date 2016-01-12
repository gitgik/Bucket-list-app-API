from rauth import OAuth1Service, OAuth2Service
from flask import url_for, current_app, request, redirect, session


class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for(
            'oauth_callback',
            provider=self.provider_name,
            _external=True)

    @classmethod
    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]


class FacebookSignIn(OAuthSignIn):
    """Signs in using Facebook Oauth service"""
    def __init__(self):
        super(FacebookSignIn, self).__init__('facebook')
        # Initialize service object with client_id and client_secret
        self.service = OAuth2Service(
            name='facebook',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://graph.facebook.com/oauth/authorize',
            access_token_url='https://graph.facebook.com/oauth/access_token',
            base_url='https://graph.facebook.com/'
        )

    def authorize(self):
        """Issues a redirect to a URL provided by the Rauth's service object
        Invokes the route after authentication completes
        """
        return redirect(self.service.get_authorize_url(
            scope='email',
            response_type='code',
            redirect_url=self.get_callback_url())
        )

    def callback(self):
        if 'code' not in request.args:
            return None, None, None
        oauth_session = self.service.get_auth_session(
            data={
                'code': request.args['code'],
                'grant_type': 'authorization_code',
                'redirect_uri': self.get_callback_url()
            }
        )
        me = oauth_session.get('me?fields=id, email').json()
        # extract email's user because Fb doesn't
        # provide usernames by default.
        return (
            'facebook$' + me['id'],
            me.get('email').split('@')[0],
            me.get('email')
        )


class TwitterSignIn(OAuthSignIn):
    pass
