from auth import *

stringify = lambda x : '"' + x + '"'

def get_data(g, sql):
    cursor = g.db.cursor()
    cursor.execute(sql)
    data = [dict((cursor.description[idx][0], value) for idx, value in enumerate(row)) for row in cursor.fetchall()]
    return data

def get_user(g, username):
    sql = 'select * from users where username = "%s"' % username
    user = get_data(g, sql)
    user = User(user[0])
    return user

def get_user_by_id(g, user_id):
    sql = 'select * from users where userid = %s' % user_id
    user = get_data(g, sql)
    user = User(user[0])
    return user

