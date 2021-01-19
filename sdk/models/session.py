import datetime

from flask import session

from sdk.constants.common import ISSUER
from sdk.constants.endpoints import AUTHORIZATION_ENDPOINT, TOKEN_ENDPOINT, \
    END_SESSION_ENDPOINT, JWKS_ENDPOINT, \
    REVOKE_TOKEN_ENDPOINT, OP_CONFIG_INITIATED, TENANT
from sdk.constants.token import ACCESS_TOKEN, ACCESS_TOKEN_EXPIRE_IN, \
    ACCESS_TOKEN_ISSUED_AT, ID_TOKEN, REFRESH_TOKEN, \
    SCOPE, TOKEN_TYPE
from sdk.constants.user import DISPLAY_NAME, EMAIL, USERNAME


def remove_session_parameter(key):
    if key in session:
        session.pop(key)


def set_session_parameter(key, value):
    session[key] = value


def get_session_parameter(key):
    if key in session:
        return session.get(key)
    return None


def reset_op_configuration():
    remove_session_parameter(AUTHORIZATION_ENDPOINT)
    remove_session_parameter(TOKEN_ENDPOINT)
    remove_session_parameter(END_SESSION_ENDPOINT)
    remove_session_parameter(JWKS_ENDPOINT)
    remove_session_parameter(REVOKE_TOKEN_ENDPOINT)
    remove_session_parameter(OP_CONFIG_INITIATED)
    remove_session_parameter(ISSUER)
    remove_session_parameter(TENANT)


def end_authenticated_session():
    remove_session_parameter(ACCESS_TOKEN)
    remove_session_parameter(ACCESS_TOKEN_EXPIRE_IN)
    remove_session_parameter(ACCESS_TOKEN_ISSUED_AT)
    remove_session_parameter(DISPLAY_NAME)
    remove_session_parameter(EMAIL)
    remove_session_parameter(ID_TOKEN)
    remove_session_parameter(REFRESH_TOKEN)
    remove_session_parameter(SCOPE)
    remove_session_parameter(TOKEN_TYPE)
    remove_session_parameter(USERNAME)


def init_user_session(token_response, authenticated_user):
    end_authenticated_session()
    set_session_parameter(ACCESS_TOKEN, token_response.accessToken)
    set_session_parameter(ACCESS_TOKEN_EXPIRE_IN, token_response.expiresIn)
    _UTCNOW = datetime.datetime.utcnow
    set_session_parameter(ACCESS_TOKEN_ISSUED_AT, _UTCNOW().ctime())
    set_session_parameter(DISPLAY_NAME, authenticated_user.displayName)
    set_session_parameter(EMAIL, authenticated_user.email)
    set_session_parameter(ID_TOKEN, token_response.idToken)
    set_session_parameter(SCOPE, token_response.scope)
    set_session_parameter(REFRESH_TOKEN, token_response.refreshToken)
    set_session_parameter(TOKEN_TYPE, token_response.tokenType)
    set_session_parameter(USERNAME, authenticated_user.username)
