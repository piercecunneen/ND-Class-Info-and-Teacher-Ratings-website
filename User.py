from flask.ext.login import LoginManager, UserMixin, login_required

class User(UserMixin):
    user_database = {"pcunneen@nd.edu": ("pcunneen@nd.edu", "5BrnH+"), "JaneDoe": ("Jane", "Doe")}

    def __init__(self, username, password):
        self.id = username
        self.password = password
        self.authenticated = True
        self.active = True

    @classmethod
    def get(cls, id):

        if cls.user_database.get(id):
            return User(*cls.user_database.get(id))
        else:
            return None
