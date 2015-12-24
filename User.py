from flask.ext.login import LoginManager, UserMixin, login_required
import sqlite3 as lite
database = 'reviews.sqlite'
class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.authenticated = True
        self.active = True

    @classmethod
    def get(cls, id, is_email):
        if Check_For_ID(id, is_email):
            return User(id)
        else:
            return None


def Check_For_ID(id, is_email):
    conn = lite.connect(database)
    with conn:
        c = conn.cursor()
        if is_email:
            query = "select username from userInfo where email = " + "'" + str(id) + "'"
        else:
            query = "select username from userInfo where username = " + "'" + str(id) + "'"
        c.execute(query)
        profReviews = c.fetchall()
        if profReviews:
            return True
        else:
            return False

