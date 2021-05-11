name = 'Asgardeo Auth Python SDK'
packages = ('asgardeo_auth_python_sdk', 'asgardeo_auth_python_sdk.*')
version = "0.0.16-dev0"
author = 'Asgardeo'
homepage = 'https://github.com/asgardeo/asgardeo-auth-python-sdk#readme'
license_name = 'Apache-2.0'
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
