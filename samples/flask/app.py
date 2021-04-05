""" Sample Flask based application for Asgardeo OIDC SDK.

This application demonstrates Asgardeo OIDC SDK capabilities.

"""

from functools import wraps
from http.client import HTTPException

from flask import Flask, redirect, jsonify, url_for, render_template

from samples.flask.conf import auth_config
from asgardeo_auth_python_sdk.Integration.flask_client import FlaskAsgardeoAuth
from asgardeo_auth_python_sdk.exception.asgardeo_auth_error import \
    AsgardeoAuthError
from samples.flask.constants import REDIRECT, TOKEN_RESPONSE, USERNAME

app = Flask(__name__)
app.secret_key = 'super_secret_key'

# initialize the app
identity_auth = FlaskAsgardeoAuth(auth_config=auth_config)


def requires_auth(f):
    """
    Decorator to secure the protected endpoint which require user
    authentication.

    Args:
        f : function to be decorated
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        """
        Decorator to redirect user to the dashboard.
        """
        if not identity_auth.is_session_data_available(USERNAME):
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)

    return decorated


@app.errorhandler(Exception)
def handle_auth_error(ex):
    """
    Handle an authentication error.

    Args:
        ex : Exception to handle.
    """
    response = jsonify(message=str(ex))
    response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
    return response


@app.route('/')
@requires_auth
def home():
    """
    Render the login page.
    """
    session_data = identity_auth.get_post_auth_session_data()
    return render_template('/dashboard.html', session_data=session_data)


@app.route('/signin')
def dashboard():
    """
    Render the dashboard page.
    """
    return render_template('/index.html')


@app.route('/login')
def login():
    """
    Login to implementation from asgardeo_auth_python_sdk.
    """
    response = identity_auth.sign_in()
    if REDIRECT in response:
        return redirect(response[REDIRECT])
    elif TOKEN_RESPONSE in response:
        credentials, authenticated_user = response[TOKEN_RESPONSE]
        return redirect(url_for('home'))
    else:
        raise AsgardeoAuthError(
            'Error occurred on the sign in Process Please Try again later')


@app.route('/logout')
def logout():
    """
    Logout implementation from asgardeo_auth_python_sdk.
    """
    return identity_auth.sign_out()


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')
