class AuthenticatedUser:

    def __init__(self, display_name, email, username):
        self.display_name: str = display_name
        self.email: str = email
        self.username: str = username

    def get_user(self):
        return self.__dict__
