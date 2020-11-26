from functools import wraps
from http.client import HTTPException

from flask import Flask, redirect, jsonify, url_for, \
    render_template

from samples.flask.conf import auth_config
from sdk.Integration.flask_client.identity_auth import FlaskIdentityAuth
from sdk.constants.common import REDIRECT, TOKEN_RESPONSE
from sdk.constants.user import USERNAME
from sdk.exception.identityautherror import IdentityAuthError

app = Flask(__name__)
app.secret_key = 'super_secret_key'

identity_auth = FlaskIdentityAuth(auth_config=auth_config)


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not identity_auth.is_session_data_available(USERNAME):
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)

    return decorated


@app.errorhandler(Exception)
def handle_auth_error(ex):
    response = jsonify(message=str(ex))
    response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
    return response


@app.route('/')
@requires_auth
def home():
    session_data = identity_auth.get_post_auth_session_data()
    return render_template('/dashboard.html', session_data=session_data)


@app.route('/signin')
def dashboard():
    return render_template('/index.html')


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


@app.route('/logout')
def logout():
    return identity_auth.sign_out()


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=3000)
    app.run()
