from flask.ext.login import UserMixin






class User():

    def __init__(self, user):
        self.user_id = user['UserID']
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
        self.tweets = user['Tweets']

    def is_authenticated(self):
            return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.user_id)

    def __repr__(self):
        return '<User %r>' % self.username



