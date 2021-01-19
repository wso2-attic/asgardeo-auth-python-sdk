"""This module keeps the minimal required configuration sample to initialize
the client. """

auth_config = {
    "login_callback_url": "http://localhost:5000/login",
    "logout_callback_url": "http://localhost:5000/signin",
    "client_host": "https://localhost:5000",
    "client_id": "<client_id>",
    "client_secret": "<client_secret>",
    "server_origin": "http://localhost:9443",
    "tenant_path": "/t/wso2.com",
    "tenant": "wso2.com"
}
