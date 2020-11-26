# WSO2 Identity Server - OIDC Flask SDK  Usage Example
---

### Register an Application

Run Developer Portal and register a Web Application with minimal configuration. 
Give `http://localhost:5000/login` as the callback URL.

### Setup and run sample

1. Update your configurations in `config.py` with WSO2 Identity Server App Register details.

    E.g.

    ```python
    auth_config = {
        "login_callback_url": "http://127.0.0.1:5000/login",
        "logout_callback_url": "http://127.0.0.1:5000/signin",
        "client_host": "https://127.0.0.1:5000",
        "client_id": "<client_id>",
        "client_secret": "client_secret",
        "server_origin": "https://localhost:9443",
        "tenant_path": "/t/<tenant>",
        "tenant": "<tenant>"
    }
    ```

2. Initialize the sdk
    ```python
    identity_auth = FlaskIdentityAuth(auth_config=auth_config)
    ```


3. Add signin implementation
    ```python
    @app.route("/login")
    def login():
        response = identity_auth.sign_in()
        if REDIRECT in response:
            return redirect(response[REDIRECT])
        elif TOKEN_RESPONSE in response:
            credentials, authenticated_user = response[TOKEN_RESPONSE]
            return redirect(url_for('home'))
        else:
            raise IdentityAuthError("Error occurred on the sign in Process Please Try again later")
   ```

4. Add signout implementation
    ```python
   @app.route('/logout')
    def logout():
        return identity_auth.sign_out()
   ```

5. Navigate to `http://localhost:5000` from the browser
