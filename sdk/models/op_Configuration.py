import http
import ssl

import requests

from sdk.constants.common import ISSUER, TRUE_STRING
from sdk.constants.endpoints import AUTHORIZATION_ENDPOINT, TOKEN_ENDPOINT, JWKS_ENDPOINT, REVOKE_TOKEN_ENDPOINT, \
    TENANT, END_SESSION_ENDPOINT, SERVICE_RESOURCES, OP_CONFIG_INITIATED, INTROSPECTION_ENDPOINT
from sdk.constants.user import USERNAME
from sdk.exception.identityautherror import IdentityAuthError
from sdk.models.session import remove_session_parameter, get_session_parameter, set_session_parameter


def is_op_config_initiated():
    return get_session_parameter(OP_CONFIG_INITIATED) and get_session_parameter(OP_CONFIG_INITIATED) == TRUE_STRING


def set_authorize_endpoint(authorization_endpoint):
    set_session_parameter(AUTHORIZATION_ENDPOINT, authorization_endpoint)


def set_token_endpoint(token_endpoint):
    set_session_parameter(TOKEN_ENDPOINT, token_endpoint)


def set_end_session_endpoint(end_session_endpoint):
    set_session_parameter(END_SESSION_ENDPOINT, end_session_endpoint)


def set_jwks_uri(jwks_endpoint):
    set_session_parameter(JWKS_ENDPOINT, jwks_endpoint)


def set_revoke_token_endpoint(revoke_token_endpoint):
    set_session_parameter(REVOKE_TOKEN_ENDPOINT, revoke_token_endpoint)


def set_opconfig_initiated():
    set_session_parameter(OP_CONFIG_INITIATED, TRUE_STRING)


def set_tenant(tenant):
    set_session_parameter(TENANT, tenant)


def set_issuer(issuer):
    set_session_parameter(ISSUER, issuer)


def get_authorize_endpoint():
    return get_session_parameter(AUTHORIZATION_ENDPOINT)


def get_token_endpoint():
    return get_session_parameter(AUTHORIZATION_ENDPOINT)


def get_authorize_endpoint():
    return get_session_parameter(TOKEN_ENDPOINT)


def get_authorize_endpoint():
    return get_session_parameter(AUTHORIZATION_ENDPOINT)


def get_revoke_token_endpoint():
    return get_session_parameter(REVOKE_TOKEN_ENDPOINT)


def get_end_session_endpoint():
    return get_session_parameter(END_SESSION_ENDPOINT)


def get_jwks_uri():
    return get_session_parameter(JWKS_ENDPOINT)


def get_username():
    return get_session_parameter(USERNAME)


def get_tenant():
    return get_session_parameter(TENANT)


def get_issuer():
    return get_session_parameter(ISSUER)


def is_valid_opconfig(tenant):
    return is_op_config_initiated() and get_tenant() and get_tenant()==tenant





class OPConfiguration():

    def __init__(self, auth_config):

        self.op_config_initiated = False
        serverHost = auth_config.server_origin + auth_config.tenant_path
        well_known_url = serverHost + SERVICE_RESOURCES["well_known"]
        try:
            resp = requests.get(url=well_known_url, verify=ssl.CERT_NONE)
            if resp.status_code != http.client.OK:
                raise IdentityAuthError("Failed to load OpenID provider configuration from: " + well_known_url)

            resp_data = resp.json()
            self.authorization_endpoint = resp_data[AUTHORIZATION_ENDPOINT]
            self.token_endpoint = resp_data[TOKEN_ENDPOINT]
            self.end_session_endpoint = resp_data[END_SESSION_ENDPOINT]
            self.jwks_uri = resp_data[JWKS_ENDPOINT]
            self.revocation_endpoint = resp_data[REVOKE_TOKEN_ENDPOINT]
            self.introspection_endpoint = resp_data[INTROSPECTION_ENDPOINT]
            self.tenant = auth_config.tenant
            self.issuer = resp_data[ISSUER]
            self.op_config_initiated = True

        except:

            self.authorization_endpoint = serverHost + SERVICE_RESOURCES["authorize"]
            self.token_endpoint = serverHost + SERVICE_RESOURCES["token"]
            self.end_session_endpoint = serverHost + SERVICE_RESOURCES["logout"]
            self.jwks_uri = serverHost + SERVICE_RESOURCES["jwks"]
            self.revocation_endpoint = serverHost + SERVICE_RESOURCES["revoke"]
            self.introspection_endpoint = serverHost + SERVICE_RESOURCES["introspect"]
            self.tenant = SERVICE_RESOURCES["tenant"]
            self.issuer = serverHost + SERVICE_RESOURCES["token"]
            self.op_config_initiated = True

            # raise IdentityAuthError("Initialized OpenID Provider configuration from default configuration. "
            #             "Because failed to access wellknown endpoint: " + well_known_url)


    def reset_op_configuration(self):

        self.authorization_endpoint = None
        self.token_endpoint = None
        self.end_session_endpoint = None
        self.jwks_uri = None
        self.revocation_endpoint = None
        self.tenant = None
        self.issuer = None
        self.op_config_initiated = False

    def is_valid_op_config(self, tenant):

        return self.op_config_initiated and tenant == self.tenant


def reset_opconfiguration():
    remove_session_parameter(AUTHORIZATION_ENDPOINT)
    remove_session_parameter(TOKEN_ENDPOINT)
    remove_session_parameter(END_SESSION_ENDPOINT)
    remove_session_parameter(JWKS_ENDPOINT)
    remove_session_parameter(REVOKE_TOKEN_ENDPOINT)
    remove_session_parameter(OP_CONFIG_INITIATED)
    remove_session_parameter(ISSUER)
    remove_session_parameter(TENANT)


def init_op_configuration(request_params,force_init=False):

    if not force_init and is_valid_opconfig(request_params[TENANT]):
        return "OP config is already initiated"



    serverHost = request_params["serverOrigin"] + request_params["tenantPath"]
    well_known_url = serverHost + SERVICE_RESOURCES["wellKnown"]
    resp = requests.get(url=well_known_url, verify=ssl.CERT_NONE)

    try:
        if resp.status_code != http.client.OK:
            raise IdentityAuthError("Failed to load OpenID provider configuration from: " + well_known_url)
        else:
            resp_data = resp.json()
            set_authorize_endpoint(resp_data[AUTHORIZATION_ENDPOINT])
            set_token_endpoint(resp_data[TOKEN_ENDPOINT])
            set_end_session_endpoint(resp_data[END_SESSION_ENDPOINT])
            set_jwks_uri(resp_data[JWKS_ENDPOINT])
            set_revoke_token_endpoint(resp_data[REVOKE_TOKEN_ENDPOINT])
            set_issuer(resp_data[ISSUER])
            set_tenant(request_params[TENANT])
            set_opconfig_initiated()

    except IdentityAuthError:

        resp_data = resp.json()
        set_authorize_endpoint(request_params["serverOrigin"] + SERVICE_RESOURCES["authorize"])
        set_token_endpoint(request_params["serverOrigin"] + SERVICE_RESOURCES["token"])
        set_end_session_endpoint(request_params["serverOrigin"] + SERVICE_RESOURCES["logout"])
        set_jwks_uri(request_params["serverOrigin"] + SERVICE_RESOURCES["jwks"])
        set_revoke_token_endpoint(request_params["serverOrigin"] + SERVICE_RESOURCES["revoke"])
        set_issuer( request_params["serverOrigin"] + SERVICE_RESOURCES["token"])
        set_tenant(SERVICE_RESOURCES[TENANT])
        set_opconfig_initiated()


        raise IdentityAuthError("Initialized OpenID Provider configuration from default configuration. "
                    "Because failed to access wellknown endpoint: " + well_known_url)

