name = 'asgardeo-auth-python-sdk'
packages = ('asgardeo_auth', 'asgardeo_auth.*')
version = "0.1.3-dev0"
author = 'Asgardeo'
homepage = 'https://github.com/asgardeo/asgardeo-auth-python-sdk#readme'
license_name = 'Apache Software License'
description = "Asgardeo Auth Python SDK."
bug_tracker = 'https://github.com/asgardeo/asgardeo-auth-python-sdk/issues'
keywords = [
    "Asgardeo",
    "OIDC",
    "OAuth2",
    "Authentication",
    "Authorization"
]
download_url = 'https://github.com/asgardeo/asgardeo-auth-python-sdk/releases'
author = "Asgardeo",
author_email = "beta@asgardeo.io"
default_user_agent = '{}/{} (+{})'.format(name, version, homepage)
default_json_headers = [
    ('Content-Type', 'application/json'),
    ('Cache-Control', 'no-store'),
    ('Pragma', 'no-cache'),
]
