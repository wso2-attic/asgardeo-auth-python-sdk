from flask import session

from sdk.framework import Framework


class FlaskFramework(Framework):

    def __init__(self, name="wso2_is {}"):
        self.name = name

    def set_session_data(self, request, key, value):
        sess_key = self.name.format(key)
        session[sess_key] = value

    def get_session_data(self, request, key):
        sess_key = self.name.format(key)
        return session.get(sess_key, None)

    def is_session_data_available(self, request, key):
        sess_key = self.name.format(key)
        return sess_key in session

    def clear_session_data(self, request, key):
        sess_key = self.name.format(key)
        session.pop(sess_key, None)
