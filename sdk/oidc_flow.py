import datetime
import ssl
import urllib
from venv import logger

import requests
import http as http_lib

from sdk import _helpers, pkce
from sdk._helpers import parse_exchange_token_response
from sdk.common.security import generate_token
from sdk.constants.token import OIDC_SCOPE
from sdk.exception.identityautherror import IdentityAuthError
from sdk.models.auth_config import AuthConfig
from sdk.models.crypto import validate_jwt
from sdk.models.op_Configuration import OPConfiguration
from sdk.models.token_response import TokenResponse, extract_id_token

_UTCNOW = datetime.datetime.utcnow


class Flow(object):
    """Base class for all Flow objects."""
    pass


class OIDCFlow(Flow):
    """Does the Web Server Flow .

    OAuth2WebServerFlow objects may be safely pickled and unpickled.
    """

    def __init__(self, auth_config: AuthConfig = None,
                 op_configuration: OPConfiguration = None,
                 user_agent=None,
                 authorization_header=None, **kwargs):
        """Constructor for OAuth2WebServerFlow.

        The kwargs argument is used to set extra query parameters on the
        auth_uri. For example, the access_type and prompt
        query parameters can be set via kwargs.

        Args:
            client_id: string, client identifier.
            client_secret: string client secret.
            scope: string or iterable of strings, scope(s) of the credentials
                   being requested.
            login_callback_url: string, Either the string 'urn:ietf:wg:oauth:2.0:oob'
                          for a non-web-based application, or a URI that
                          handles the callback from the authorization server.
            user_agent: string, HTTP User-Agent to provide for this
                        application.
            auth_uri: string, URI for authorization endpoint. For convenience
                      defaults to Google's endpoints but any OAuth 2.0 provider
                      can be used.
            token_endpoint: string, URI for token endpoint. For convenience
                       defaults to Google's endpoints but any OAuth 2.0
                       provider can be used.
            revocation_endpoint: string, URI for revoke endpoint. For convenience
                        defaults to Google's endpoints but any OAuth 2.0
                        provider can be used.
            authorization_header: string, For use with OAuth 2.0 providers that
                                  require a client to authenticate using a
                                  header value instead of passing client_secret
                                  in the POST body.
            pkce: boolean, default: False, Generate and include a "Proof Key
                  for Code Exchange" (PKCE) with your authorization and token
                  requests. This adds security for installed applications that
                  cannot protect a client_secret. See RFC 7636 for details.
            code_verifier: bytestring or None, default: None, parameter passed
                           as part of the code exchange when pkce=True. If
                           None, a code_verifier will automatically be
                           generated as part of step1_get_authorize_url(). See
                           RFC 7636 for details.
            **kwargs: dict, The keyword arguments are all optional and required
                      parameters for the OAuth calls.
        """
        # scope is a required argument, but to preserve backwards-compatibility
        # we don't want to rearrange the positional arguments
        if auth_config.scope is None:
            raise TypeError("The value of scope must not be None")

        if auth_config.client_id is None:
            raise TypeError("The value of client_id must not be None")

        if auth_config.client_id is None:
            raise TypeError("The value of client_id must not be None")

        self.auth_config: AuthConfig = auth_config
        self.op_configuration: OPConfiguration = op_configuration
        if OIDC_SCOPE not in self.auth_config.scope:
            self.auth_config.scope.append(OIDC_SCOPE)

        self.auth_config.scope_string = _helpers.scopes_to_string(self.auth_config.scope)
        self.user_agent = user_agent
        self.authorization_header = authorization_header
        self.params = _oauth2_web_server_flow_params(kwargs)

    def get_authorize_url(self, login_callback_url=None, state=None):
        """Returns a URI to redirect to the provider.

        Args:
            login_callback_url: string, Either the string 'urn:ietf:wg:oauth:2.0:oob'
                          for a non-web-based application, or a URI that
                          handles the callback from the authorization server.
                          This parameter is deprecated, please move to passing
                          the redirect_uri in via the constructor.
            state: string, Opaque state string which is passed through the
                   OAuth2 flow and returned to the client as a query parameter
                   in the callback.

        Returns:
            A URI as a string to redirect the user to begin the authorization
            flow.
        """
        if login_callback_url is not None:
            logger.warning((
                'The redirect_uri parameter for '
                'OAuth2WebServerFlow.step1_get_authorize_url is deprecated. '
                'Please move to passing the redirect_uri in via the '
                'constructor.'))
            self.auth_config.login_callback_url = login_callback_url

        if self.auth_config.login_callback_url is None:
            raise ValueError('The value of redirect_uri must not be None.')

        query_params = {
            'client_id': self.auth_config.client_id,
            'redirect_uri': self.auth_config.login_callback_url,
            'scope': self.auth_config.scope_string,
        }
        if state is None:
            state = generate_token()
        query_params['state'] = state

        if self.auth_config.enable_pkce:
            if not self.auth_config.code_verifier:
                self.auth_config.code_verifier = pkce.code_verifier()
            challenge = pkce.code_challenge(self.auth_config.code_verifier)
            query_params['code_challenge'] = challenge
            query_params['code_challenge_method'] = 'S256'

        query_params.update(self.params)

        return _helpers.update_query_params(self.op_configuration.authorization_endpoint, query_params), state

    def send_token_request(self, code=None):
        """Exchanges a code for OAuth2Credentials.

        Args:
            code: string, a dict-like object, or None. For a non-device
                  flow, this is either the response code as a string, or a
                  dictionary of query parameters to the redirect_uri. For a
                  device flow, this should be None.

        Returns:
            An OAuth2Credentials object that can be used to authorize requests.

        Raises:
            FlowExchangeError: if a problem occurred exchanging the code for a
                               refresh_token.
            ValueError: if code and device_flow_info are both provided or both
                        missing.
        """
        if code is None:
            raise ValueError('No code provided.')

        if not self.op_configuration.token_endpoint:
            raise ValueError('Invalid token endpoint found.')

        post_data = {
            'client_id': self.auth_config.client_id,
            'code': code,
            'scope': self.auth_config.scope_string,
        }
        if self.auth_config.client_secret is not None:
            post_data['client_secret'] = self.auth_config.client_secret
        if self.auth_config.enable_pkce:
            post_data['code_verifier'] = self.auth_config.code_verifier
        else:
            post_data['grant_type'] = 'authorization_code'
            post_data['redirect_uri'] = self.auth_config.login_callback_url
        body = urllib.parse.urlencode(post_data)

        headers = self.get_token_request_headers()

        resp = requests.post(self.op_configuration.token_endpoint, data=body, headers=headers, verify=ssl.CERT_NONE)
        content = resp.content
        data_response = parse_exchange_token_response(content)
        if resp.status_code == http_lib.client.OK and 'access_token' in data_response:
            return self.get_token_response_from_resp(data_response)
        else:
            logger.info('Failed to retrieve access token: %s', content)
            if 'error' in data_response:
                # you never know what those providers got to say
                error_msg = (str(data_response['error']) +
                             str(data_response.get('error_description', '')))
            else:
                error_msg = 'Invalid response: {0}.'.format(str(resp.status))
            raise IdentityAuthError(error_msg)

    def send_authorization_request(self):

        url, state = self.get_authorize_url()
        result = {
            'url': url,
            'state': state
        }
        return result

    def get_token_request_headers(self):

        headers = {
            'content-type': 'application/x-www-form-urlencoded',
        }
        if self.authorization_header is not None:
            headers['Authorization'] = self.authorization_header
        if self.user_agent is not None:
            headers['user-agent'] = self.user_agent
        return headers

    def validate_id_token(self, id_token, client_id, issuer):

        jwks_endpoint = self.op_configuration.jwks_uri
        if not jwks_endpoint and not len(jwks_endpoint):
            raise IdentityAuthError("Invalid JWKS URI found.")
        resp = requests.get(url=jwks_endpoint, verify=ssl.CERT_NONE)
        try:
            if resp.status_code != http_lib.client.OK:
                raise IdentityAuthError("Failed to load public keys from JWKS URI " + jwks_endpoint)

            keys = resp.json()["keys"]
            return validate_jwt(id_token, keys, client_id, issuer)
        except IdentityAuthError:
            raise IdentityAuthError("Failed to validate the ID Token")

    def send_refresh_token_request(self, refresh_token):
        token_endpoint = self.op_configuration.token_endpoint
        if not token_endpoint:
            raise IdentityAuthError("Invalid token endpoint found.")

        post_data = {
            'client_id': self.auth_config.client_id,
            'refresh_token': refresh_token,
            'grant_type': "refresh_token",
        }

        headers = self.get_token_request_headers()

        resp = requests.post(token_endpoint, data=post_data, headers=headers, verify=ssl.CERT_NONE)
        content = resp.content
        data_response = parse_exchange_token_response(content)
        if resp.status_code != http_lib.client.OK and 'access_token' in data_response:
            raise IdentityAuthError("Invalid status code received in the refresh token response: " + str(resp.status_code))
        return self.get_token_response_from_resp(data_response)

    def get_token_response_from_resp(self, resp):
        access_token = resp['access_token']
        refresh_token = resp.get('refresh_token', None)
        if not refresh_token:
            logger.info(
                'Received token response with no refresh_token. Consider '
                "reauthenticating with prompt='consent'.")
        token_expiry = None
        if 'expires_in' in resp:
            delta = datetime.timedelta(seconds=int(resp['expires_in']))
            token_expiry = delta + _UTCNOW()

        extracted_id_token = None
        id_token_jwt = None
        if 'id_token' in resp:
            extracted_id_token = extract_id_token(resp['id_token'])
            id_token_jwt = resp['id_token']

        logger.info('Successfully retrieved access token')
        decoded_payload = self.validate_id_token(id_token_jwt, self.auth_config.client_id, self.op_configuration.issuer)
        return TokenResponse(
            access_token, self.auth_config.client_id, self.auth_config.client_secret,
            refresh_token, token_expiry, self.op_configuration.token_endpoint, self.user_agent,
            revoke_uri=self.op_configuration.revocation_endpoint, id_token=extracted_id_token,
            id_token_jwt=id_token_jwt, token_response=resp, scopes=self.auth_config.scope_string,
            introspection_endpoint=self.op_configuration.introspection_endpoint, decoded_payload=decoded_payload)

    def send_revoke_token_request(self, access_token):

        revocation_endpoint = self.op_configuration.revocation_endpoint

        if not revocation_endpoint or not len(revocation_endpoint.strip()):
            raise IdentityAuthError("Invalid revoke token endpoint found.")

        post_data = {
            'client_id': self.auth_config.client_id,
            'token': access_token,
            'token_type_hint': "access_token",
        }

        headers = self.get_token_request_headers()

        resp = requests.post(revocation_endpoint, data=post_data, headers=headers,
                             verify=ssl.CERT_NONE)
        if resp.status_code != http_lib.client.OK:
            raise IdentityAuthError("Invalid status code received in the revoke token response: " + str(resp.status_code))
        return resp.json()

    def get_logout_url(self, logout_callback_url=None, id_token=None):
        """Returns a URI to redirect to the provider.

        Args:
            login_callback_url: string, Either the string 'urn:ietf:wg:oauth:2.0:oob'
                          for a non-web-based application, or a URI that
                          handles the callback from the authorization server.
                          This parameter is deprecated, please move to passing
                          the redirect_uri in via the constructor.
            state: string, Opaque state string which is passed through the
                   OAuth2 flow and returned to the client as a query parameter
                   in the callback.

        Returns:
            A URI as a string to redirect the user to begin the authorization
            flow.
        """


        logout_endpoint = self.op_configuration.end_session_endpoint

        if not logout_endpoint:
            raise IdentityAuthError("No logout endpoint found in the session.")

        if not id_token:
            raise IdentityAuthError("Invalid id_token found in the session.")

        if logout_callback_url is not None:
            logger.warning((
                'The redirect_uri parameter for '
                'OAuth2WebServerFlow.step1_get_authorize_url is deprecated. '
                'Please move to passing the redirect_uri in via the '
                'constructor.'))
            self.auth_config.logout_callback_url = logout_callback_url

        if not self.auth_config.logout_callback_url:
            raise ValueError('The value of redirect_uri must not be None.')

        query_params = {
            'post_logout_redirect_uri': self.auth_config.logout_callback_url,
            'id_token_hint': id_token
        }

        return _helpers.update_query_params(logout_endpoint, query_params)


def _oauth2_web_server_flow_params(kwargs):
    """Configures redirect URI parameters for OAuth2WebServerFlow."""
    params = {
        'access_type': 'offline',
        'response_type': 'code',
    }

    params.update(kwargs)

    # Check for the presence of the deprecated approval_prompt param and
    # warn appropriately.
    approval_prompt = params.get('approval_prompt')
    if approval_prompt is not None:
        logger.warning(
            'The approval_prompt parameter for OAuth2WebServerFlow is '
            'deprecated. Please use the prompt parameter instead.')

        if approval_prompt == 'force':
            logger.warning(
                'approval_prompt="force" has been adjusted to '
                'prompt="consent"')
            params['prompt'] = 'consent'
            del params['approval_prompt']

    return params
