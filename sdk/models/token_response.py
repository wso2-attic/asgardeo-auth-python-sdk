import json

from sdk import _helpers
from sdk.exception.identityautherror import IdentityAuthError


class Credentials(object):
    """Base class for all Credentials objects.
    """


class TokenResponse(Credentials):
    """Credentials object for OAuth 2.0.
    """

    def __init__(self, access_token, client_id, client_secret, refresh_token,
                 token_expiry, token_uri, user_agent, revoke_uri=None,
                 id_token=None, token_response=None, scopes=None,
                 introspection_endpoint=None, id_token_jwt=None, decoded_payload=None):
        """Create an instance of OAuth2Credentials.

        This constructor is instantiated by the OIDC_FLOW.

        Args:
            access_token: string, access token.
            client_id: string, client identifier.
            client_secret: string, client secret.
            refresh_token: string, refresh token.
            token_expiry: datetime, when the access_token expires.
            token_uri: string, URI of token endpoint.
            user_agent: string, The HTTP User-Agent to provide for this
                        application.
            revoke_uri: string, URI for revoke endpoint. Defaults to None; a
                        token can't be revoked if this is None.
            id_token: object, The identity of the resource owner.
            token_response: dict, the decoded response to the token request.
                            None if a token hasn't been requested yet. Stored
                            because some providers (e.g. wordpress.com) include
                            extra fields that clients may want.
            scopes: list, authorized scopes for these credentials.
            introspection_endpoint: string, the URI for the token info endpoint.
                            Defaults to None; scopes can not be refreshed if
                            this is None.
            id_token_jwt: string, the encoded and signed identity JWT. The
                          decoded version of this is stored in id_token.

        Notes:
            store: callable, A callable that when passed a Credential
                   will store the credential back to where it came from.
                   This is needed to store the latest access_token if it
                   has expired and been refreshed.
        """
        self.access_token = access_token
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.store = None
        self.token_expiry = token_expiry
        self.token_uri = token_uri
        self.user_agent = user_agent
        self.revoke_uri = revoke_uri
        self.id_token = id_token
        self.id_token_jwt = id_token_jwt
        self.token_response = token_response
        self.scopes = set(_helpers.string_to_scopes(scopes or []))
        self.introspection_endpoint = introspection_endpoint
        self.decoded_payload = decoded_payload

        # True if the credentials have been revoked or expired and can't be
        # refreshed.
        self.invalid = False

def extract_id_token(id_token):
    """Extract the JSON payload from a JWT.

    Does the extraction w/o checking the signature.

    Args:
        id_token: string or bytestring, OAuth 2.0 id_token.

    Returns:
        object, The deserialized JSON payload.
    """
    if type(id_token) == bytes:
        segments = id_token.split(b'.')
    else:
        segments = id_token.split(u'.')

    if len(segments) != 3:
        raise IdentityAuthError(
            'Wrong number of segments in token: {0}'.format(id_token))

    return json.loads(
        _helpers._from_bytes(_helpers._urlsafe_b64decode(segments[1])))
