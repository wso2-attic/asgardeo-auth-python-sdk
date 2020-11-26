class Framework(object):

    def __init__(self, name="wso2_is"):
        self.name = name

    def set_session_data(self, request, key, value):
        """set the session variable according to the integrated framework"""
        raise NotImplementedError()

    def get_session_data(self, request, key):
        """get the session variable according to the integrated framework"""
        raise NotImplementedError()

    def is_session_data_available(self, request, key):
        """check the availability of the session variable according to the integrated framework"""
        raise NotImplementedError()

    def clear_session_data(self, request, key):
        """check the availability of the session variable according to the integrated framework"""
        raise NotImplementedError()