"""This module keeps the minimal required configuration sample to initialize
the client. """

auth_config = {
    "login_callback_url": "https://localhost:3000/login",
    "logout_callback_url": "https://localhost:3000/signin",
    "client_host": "https://localhost:3000",
    "client_id": "<client_id>",
    "client_secret": "<client_secret>",
    "server_origin": "https://api.asgardeo.io",
    "tenant_path": "/t/<tenant>",
    "tenant": "<tenant>",
    "certificate_path": "cert/wso2.crt"
}
