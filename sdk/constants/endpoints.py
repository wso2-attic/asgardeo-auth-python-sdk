AUTHORIZATION_ENDPOINT = "authorization_endpoint"
TOKEN_ENDPOINT = "token_endpoint"
REVOKE_TOKEN_ENDPOINT = "revocation_endpoint"
END_SESSION_ENDPOINT = "end_session_endpoint"
USER_INFO_ENDPOINT = "userinfo_endpoint"
JWKS_ENDPOINT = "jwks_uri"
OP_CONFIG_INITIATED = "op_config_initiated"
INTROSPECTION_ENDPOINT = "introspection_endpoint"
TENANT = "tenant"

SERVICE_RESOURCES = {
            "authorize": "/oauth2/authorize",
            "jwks": "/oauth2/jwks",
            "logout": "/oidc/logout",
            "revoke": "/oauth2/revoke",
            "token": "/oauth2/token",
            "introspect": "/oauth2/introspect",
            "tenant": "carbon.super",
            "well_known": "/oauth2/oidcdiscovery/.well-known/openid-configuration"
        }