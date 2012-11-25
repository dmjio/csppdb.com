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
    return cursor.lastrowid

def get_data(sql):
    cursor = g.db.cursor()
    cursor.execute(sql)
    data = [dict((cursor.description[idx][0], value) for idx, value in enumerate(row)) for row in cursor.fetchall()]
    return data

def add_user(username, email, password):
    sql = "call ADD_USER(%s, %s, %s)" % (stringify(username), stringify(password), stringify(email),)
    exec_sql(sql)
    return get_user(username)

def get_tags(tag='first'):
    sql = "SELECT *, u.IMG FROM TWEETS t INNER JOIN Users u on u.Username = t.Username WHERE TWEETID IN (SELECT TWEETID FROM HASH WHERE TAG LIKE '%" + tag + "%');"
    tags = get_data(sql)
    for i in tags: i['IMG'] = gravatar_url(i['Email'], 30)
    return tags

def get_followers(username):
    sql = "SELECT * FROM Users u WHERE u.Username in (SELECT Follower FROM Followers where User = %s);" % stringify(username)
    followers = get_data(sql)
    for i in followers: i['IMG'] = gravatar_url(i['Email'], 30)
    return followers

def get_followees(username):
    sql = "SELECT * FROM Users u WHERE u.Username in (SELECT User FROM Followers where Follower = %s);" % stringify(username)
    followees = get_data(sql)
    for i in followees: i['IMG'] = gravatar_url(i['Email'], 30)
    return followees

def get_main():
    #get feed
    sql = "SELECT t.*, u.img, u.username, u.email FROM TWEETS t INNER JOIN USERS u on t.username = u.username;"
    tweets = get_data(sql)
    for i in tweets: i['img'] = gravatar_url(i['email'], 30)
    #get user info
    user = get_user(g.user.username)
    user.img = gravatar_url(user.email, 140)

    return tweets, user

def create_tweet(tweet):
    sql = "INSERT INTO TWEETS VALUES (NULL, %s, %s, NOW())" % (stringify(tweet), stringify(g.user.username),)
    cursor = g.db.cursor()
    cursor.execute(sql)
    id = cursor.lastrowid
    for word in tweet.split():
        if "#" in word:
            sql = "call ADD_HASH(%s, %s)" % (stringify(word[1:]), id,)
            exec_sql(sql)
    for word in tweet.split():
        if "@" in word:
            sql = "call ADD_MENTION(%s, %s)" % (id, stringify(word[1:]))
            exec_sql(sql)
    for word in tweet.split():
        if ".com" in word or ".net" in word or ".org" in word or ".co.uk" in word or ".biz" in word:
            sql = "call ADD_URL(%s, %s)" % (stringify(word), id,)
            exec_sql(sql)

def get_people_to_follow(user):
    sql = "SELECT * FROM USERS u WHERE u.Username NOT IN (SELECT f.User from FOLLOWERS f where f.Follower = %s) and u.Username != %s;" % (stringify(user), stringify(user))
    users = get_data(sql)
    return users

def unfollow_user(follower, username):
    sql = "call UNFOLLOW_USER(%s, %s)" % (stringify(follower),stringify(username),)
    exec_sql(sql)

def follow_user(follower, username):
    sql = "call FOLLOW_USER(%s, %s)" % (stringify(username), stringify(follower),)
    exec_sql(sql)

def get_top_ten_recent_tags():
    sql = "SELECT * FROM TWEETs WHERE TWEETID IN (SELECT TweetID FROM HASH ORDER BY CREATED DESC) LIMIT 10;"
    return get_data(sql)

def get_user(username):
    sql = 'select * from users u where u.username = %s' % stringify(username)
    user = get_data(sql)
    if len(user) and user[0] is not None:
        return User(user[0])
    else:
        return None

def get_follower_info(username):
    sql = 'select count(*) as "count" from followers f where f.user = %s' % stringify(username)
    people_that_follow_me = get_data(sql)
    sql = 'select count(*) "count" from followers f where f.follower = %s' % stringify(username)
    people_i_follow = get_data(sql)
    return people_i_follow[0]['count'], people_that_follow_me[0]['count']

def gravatar_url(email, size=80):
    """Return the gravatar image for the given email address."""
    return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%d' %\
           (md5(email.strip().lower().encode('utf-8')).hexdigest(), size)

def format_datetime(timestamp):
    """Format a timestamp for display."""
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d @ %H:%M')


def format_date(timestamp):
    """Format a timestamp for display."""
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')