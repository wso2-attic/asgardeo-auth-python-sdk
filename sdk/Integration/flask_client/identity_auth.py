import logging
from functools import wraps

from flask import session, redirect

from sdk.Integration.flask_client.framework import FlaskFramework
from sdk.constants.common import TOKEN_RESPONSE, REDIRECT
from sdk.constants.token import ACCESS_TOKEN, ID_TOKEN, AUTHORIZATION_CODE, STATE
from sdk.constants.user import USERNAME
from sdk.exception.identityautherror import IdentityAuthError
from sdk.identity_auth import IdentityAuth
from flask import request as flask_req

logger = logging.getLogger(__name__)


class FlaskIdentityAuth(IdentityAuth):
    """
    IdentityAuth class.
    """

    def __init__(self, auth_config):
        framework = FlaskFramework()
        super().__init__(auth_config, framework)

    def prepare_params_for_workflow(self):

        constructor_kwargs = dict(redirect_uri=self.auth_config["logout_callback_url"],
                                  op_configuration=self.op_configuration, pkce=self.auth_config["enable_pkce"],
                                  prompt=self.auth_config["prompt"], code_verifier=None)
        return constructor_kwargs

    def sign_in(self):

        result = {}
        if self.framework.is_session_data_available(flask_req,
                                                    ACCESS_TOKEN) and self.framework.is_session_data_available(
            flask_req, ID_TOKEN):
            if self.op_configuration.is_valid_op_config(self.auth_config.tenant):
                result[REDIRECT] = self.send_sign_out_request()
                return result
            else:
                result[TOKEN_RESPONSE] = self.oidc_flow.get_authenticated_user(
                    self.framework.get_session_data(flask_req, ID_TOKEN))
            return result
        else:
            code = self.get_authorization_code(flask_req)
            response = self.send_sign_in_request(flask_req, code)
            return response

    def get_authorization_code(self, request):
        """Retrieve parameters for fetching access token, those parameters come
        from request and previously saved temporary data in session.
        """
        code = None
        request_state = None
        if request.method == 'GET':
            if request.args.get(AUTHORIZATION_CODE):
                code = request.args[AUTHORIZATION_CODE]
                request_state = request.args.get(STATE)
        elif request.method == 'POST':
            if request.form and request.form.get(AUTHORIZATION_CODE):
                code = request.form[AUTHORIZATION_CODE]
                request_state = request.form.get(STATE)
        if code:
            self.validate_state_param(request, request_state)
            return code

        if AUTHORIZATION_CODE in session:
            return session[AUTHORIZATION_CODE]

        return None

    def validate_state_param(self, request, request_state):

        state = self.framework.get_session_data(request, STATE)
        if state != request_state:
            raise IdentityAuthError("CSRF Warning! State not equal in request and response.")

    def send_refresh_token_request(self, refresh_token):
        self.oidc_flow.send_refresh_token_request(refresh_token)

    def sign_out(self):
        return redirect(self.send_sign_out_request())


    def is_session_data_available(self, key):
        return self.framework.is_session_data_available(None, key)


    # def requires_auth(self,f):
    #     @wraps(f)
    #     def decorated(*args, **kwargs):
    #         if not self.framework.is_session_data_available(None, USERNAME):
    #             return redirect(self.auth_config.client_host)
    #         return f(*args, **kwargs)
    #     return decorated
