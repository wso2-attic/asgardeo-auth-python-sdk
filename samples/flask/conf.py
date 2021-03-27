"""This module keeps the minimal required configuration sample to initialize
the client. """

auth_config = {
    "login_callback_url": "https://localhost:5000/login",
    "logout_callback_url": "https://localhost:5000/signin",
    "client_host": "https://localhost:5000",
    "client_id": "u4SHfHP772VBYhSffz7hDrX7QiQa",
    "client_secret": "EU_tx0VLEfzTattupXFbeZqO3_0a",
    "server_origin": "https://localhost:9443",
    "tenant_path": "/t/wso2.com",
    "tenant": "wso2.com",
    "certificate_path": "samples/flask/cert/wso2.crt"
}
