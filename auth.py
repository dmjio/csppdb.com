from flask.ext.login import UserMixin, AnonymousUser

class Anonymous(AnonymousUser):
    name = u"Anonymous"

class User(UserMixin):

    def __init__(self, user):
        self.username = user['Username']
        self.email = user['Email']
        self.first = user['First']
        self.last = user['Last']
        self.password = user['Password']
        self.web = user['Web']
        self.created = user['Created']
        self.updated = user['Updated']
        self.blurb = user['Blurb']
        self.img = user['IMG']
        self.tweets = user['Age']
        self.active = True

    def get_id(self):
        return unicode(self.username)

    def __repr__(self):
        return '<User %r>' % self.username




