import logging

from sdk.constants.common import AUTHORIZATION_CODE_TYPE, LOGIN_SCOPE, HUMAN_TASK_SCOPE, DEFAULT_SUPER_TENANT, \
    TOKEN_RESPONSE, REDIRECT, URL, USER
from sdk.constants.token import STATE, ACCESS_TOKEN, ID_TOKEN, ID_TOKEN_JWT
from sdk.constants.user import USERNAME
from sdk.exception.identityautherror import IdentityAuthError
from sdk.models.auth_config import AuthConfig
from sdk.models.authenticated_user import AuthenticatedUser
from sdk.models.op_Configuration import OPConfiguration
from sdk.models.token_response import TokenResponse
from sdk.oidc_flow import OIDCFlow

logger = logging.getLogger(__name__)

DefaultConfig = {
    "authorization_type": AUTHORIZATION_CODE_TYPE,
    "client_secret": None,
    "consent_denied": False,
    "enable_pkce": True,
    "response_mode": None,
    "scope": [LOGIN_SCOPE, HUMAN_TASK_SCOPE],
    "tenant": DEFAULT_SUPER_TENANT,
    "tenant_path": "",
    "prompt": ""
}

post_auth_session_keys = [
    USER, ACCESS_TOKEN, ID_TOKEN, ID_TOKEN_JWT,
    USERNAME
]

"""
Ensure a class only has one instance, and provide a global point of
access to it.
"""


class IdentityAuthBase(type):
    """
    Define an Instance operation that lets clients access its unique
    instance.
    """

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class IdentityAuth(metaclass=IdentityAuthBase):
    """
    IdentityAuth class.
    """

    def __init__(self, auth_config, framework):

        self.framework = framework
        self.auth_config: AuthConfig = AuthConfig(auth_config)
        self.op_configuration: OPConfiguration = OPConfiguration(self.auth_config)
        self.credentials = None
        self.oidc_flow: OIDCFlow = OIDCFlow(self.auth_config, self.op_configuration)
        self.token_response: TokenResponse = None

    def prepare_params_for_workflow(self):

        constructor_kwargs = dict(redirect_uri=self.auth_config["logout_callback_url"],
                                  op_configuration=self.op_configuration, pkce=self.auth_config["enable_pkce"],
                                  prompt=self.auth_config["prompt"], code_verifier=None)
        return constructor_kwargs

    def sign_in(self, request):
        """Let the framework do the logic and call the send_sign_in_request with code
        The logic should be as follows:
        Check whether the session available and ID token available
            if yes :
                return the user details, id token etc.
            else:
                return calling the "send_sign_in_request"

        Before calling the send_sign_in_request you must ensure you extracted the code from the request.
        Should check whether request has the code.
        """
        raise NotImplementedError()

    def send_sign_in_request(self, request, code):

        result = {}
        if code:
            self.token_response = self.oidc_flow.send_token_request(code)
            authenticated_user = self.get_authenticated_user(self.token_response.decoded_payload)
            self.set_post_auth_session_data(user=authenticated_user.get_user(), username=authenticated_user.username,
                                            access_token=self.token_response.access_token,
                                            id_token=self.token_response.id_token,
                                            id_token_jwt=self.token_response.id_token_jwt)
            result[TOKEN_RESPONSE] = self.token_response, authenticated_user
        else:
            response = self.oidc_flow.send_authorization_request()
            self.save_authorize_data(request=request, redirect_uri=self.auth_config.login_callback_url, **response)
            result[REDIRECT] = response[URL]
        return result

    def get_authorization_code(self, request):
        """Retrieve parameters for fetching access token, those parameters come
        from request and previously saved temporary data in session.
        """
        raise NotImplementedError()

    def save_authorize_data(self, request, **kwargs):
        """Save temporary data into session for the authorization step. These
        data can be retrieved later when fetching access token.
        """
        logger.debug('Saving authorize data: {!r}'.format(kwargs))
        keys = [
            'redirect_uri', 'request_token',
            'state', 'code_verifier', 'nonce'
        ]
        for k in kwargs:
            if k in keys:
                self.framework.set_session_data(request, k, kwargs[k])

    def validate_state_param(self, request, request_state):

        state = self.framework.get_session_data(request, STATE)
        if state != request_state:
            raise IdentityAuthError("CSRF Warning! State not equal in request and response.")

    def get_authenticated_user(self, decoded_payload):

        params = {
            "display_name": decoded_payload.get("preferred_username", decoded_payload.get("sub", None)),
            "email": decoded_payload.get("email", None),
            "username": decoded_payload.get("sub", None)
        }

        return AuthenticatedUser(**params)

    def send_refresh_token_request(self, refresh_token):
        self.oidc_flow.send_refresh_token_request(refresh_token)

    def set_post_auth_session_data(self, **kwargs):
        """Save temporary data into session for the User information and the token. These
        data can be retrieved later when fetching access token.
        """
        for k in kwargs:
            if k in post_auth_session_keys:
                self.framework.set_session_data(None, k, kwargs[k])

    def clear_post_auth_session_data(self):
        """Save temporary data into session for the User information and the token. These
        data can be retrieved later when fetching access token.
        """
        for k in post_auth_session_keys:
            self.framework.clear_session_data(None, k)

    def get_post_auth_session_data(self):
        """Save temporary data into session for the User information and the token. These
        data can be retrieved later when fetching access token.
        """
        result = {}
        for k in post_auth_session_keys:
            result[k] = self.framework.get_session_data(None, k)
        return result

    def sign_out(self):
        """Let the framework do the logic and call the send_sign_in_request with code
        The logic should be as follows:
        Check whether the session available and ID token available
            if yes :
                return the user details, id token etc.
            else:
                return calling the "send_sign_in_request"

        Before calling the send_sign_in_request you must ensure you extracted the code from the request.
        Should check whether request has the code.
        """
        raise NotImplementedError()

    def send_sign_out_request(self):
        id_token = self.framework.get_session_data(None,ID_TOKEN_JWT)
        if not id_token:
            return self.auth_config.login_callback_url
        self.clear_post_auth_session_data()
        return self.oidc_flow.get_logout_url(id_token=id_token)
