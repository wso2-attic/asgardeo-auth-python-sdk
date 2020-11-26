from sdk.constants.common import AUTHORIZATION_CODE_TYPE, LOGIN_SCOPE, HUMAN_TASK_SCOPE, DEFAULT_SUPER_TENANT
from sdk.exception.identityautherror import IdentityAuthError

defaultConfig = {
    "login_callback_url",
    "logout_callback_url",
    "client_host",
    "authorization_type",
    "client_id",
    "client_secret",
    "consent_denied",
    "enable_pkce",
    "response_mode",
    "scope",
    "tenant",
    "tenant_path",
    "prompt",
    "server_origin",
    "code_verifier"
}


class AuthConfig:

    def __init__(self, auth_config):

        self.scope_string = None
        self.login_callback_url = None
        self.logout_callback_url = None
        self.client_host = None
        self.authorization_type = AUTHORIZATION_CODE_TYPE
        self.client_id = None
        self.client_secret = None
        self.consent_denied = False
        self.enable_pkce = False
        self.response_mode = None
        self.scope = [LOGIN_SCOPE, HUMAN_TASK_SCOPE]
        self.tenant = DEFAULT_SUPER_TENANT
        self.tenant_path = "/t/" + DEFAULT_SUPER_TENANT
        self.prompt = ""
        self.server_origin = "https://localhost:9443"
        self.code_verifier = None

        for key in auth_config:
            if key in defaultConfig:
                setattr(self, key, auth_config[key])
            else:
                raise IdentityAuthError("Improper kay value passed in the autoconfig. Please check the auth config")
