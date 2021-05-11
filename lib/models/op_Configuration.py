import http

import requests

from ..constants.common import ISSUER
from ..constants.endpoints import AUTHORIZATION_ENDPOINT, TOKEN_ENDPOINT, \
    JWKS_ENDPOINT, REVOKE_TOKEN_ENDPOINT, END_SESSION_ENDPOINT, \
    SERVICE_RESOURCES, INTROSPECTION_ENDPOINT
from ..exception.asgardeo_auth_error import AsgardeoAuthError


class OPConfiguration:

    def __init__(self, auth_config):

        self.op_config_initiated = False
        serverHost = auth_config.server_origin + auth_config.tenant_path
        well_known_url = serverHost + SERVICE_RESOURCES["well_known"]
        try:
            resp = requests.get(url=well_known_url,
                                verify=auth_config.certificate_path)
            if resp.status_code != http.client.OK:
                raise AsgardeoAuthError(
                    "Failed to load OpenID provider configuration from: " + well_known_url)

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
            self.authorization_endpoint = serverHost + SERVICE_RESOURCES[
                "authorize"]
            self.token_endpoint = serverHost + SERVICE_RESOURCES["token"]
            self.end_session_endpoint = serverHost + SERVICE_RESOURCES["logout"]
            self.jwks_uri = serverHost + SERVICE_RESOURCES["jwks"]
            self.revocation_endpoint = serverHost + SERVICE_RESOURCES["revoke"]
            self.introspection_endpoint = serverHost + SERVICE_RESOURCES[
                "introspect"]
            self.tenant = SERVICE_RESOURCES["tenant"]
            self.issuer = serverHost + SERVICE_RESOURCES["token"]
            self.op_config_initiated = True
            raise AsgardeoAuthError(
                "Initialized OpenID Provider configuration from default "
                "configuration. Because failed to access wellknown endpoint: "
                "" + well_known_url)

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
