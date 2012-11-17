from auth import *
from hashlib import md5

stringify = lambda x : '"' + x + '"'

def get_data(g, sql):
    cursor = g.db.cursor()
    cursor.execute(sql)
    data = [dict((cursor.description[idx][0], value) for idx, value in enumerate(row)) for row in cursor.fetchall()]
    return data

def get_user(g, username):
    sql = 'select * from users where username = %s;' % stringify(username)
    user = get_data(g, sql)
    if len(user) and user[0] is not None:
            return User(user[0])
    else:
        return None

def get_user_by_id(g, user_id):
    sql = 'select * from users where userid = %s;' % user_id
    user = get_data(g, sql)
    if len(user) and user[0] is not None:
        return User(user[0])
    else:
        return None

def gravatar_url(email, size=80):
    """Return the gravatar image for the given email address."""
    return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%d' %\
           (md5(email.strip().lower().encode('utf-8')).hexdigest(), size)

def format_datetime(timestamp):
    """Format a timestamp for display."""
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d @ %H:%M')

