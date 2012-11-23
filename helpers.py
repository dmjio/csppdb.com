from datetime import datetime
from app import mysql
from auth import *
from hashlib import md5
from flask import g

def connect_db(): return mysql.connect()

stringify = lambda x : '"' + x + '"'

def exec_sql(sql):
    cursor = g.db.cursor()
    cursor.execute(sql)
    g.db.commit()

def get_data(sql):
    cursor = g.db.cursor()
    cursor.execute(sql)
    data = [dict((cursor.description[idx][0], value) for idx, value in enumerate(row)) for row in cursor.fetchall()]
    return data

def add_user(username, email, password):
    sql = "call ADD_USER(%s, %s, %s)" % (stringify(username), stringify(password),stringify(email))
    exec_sql(sql)
    return get_user(username)


def get_user(username):
    sql = 'select * from users where username = %s;' % stringify(username)
    user = get_data(sql)
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

