from flask.ext.mysql import MySQL
import os
from functools import update_wrapper 
from flask import Flask, request, jsonify, session, url_for, redirect, \
     render_template, g, flash, make_response
from data import *
from werkzeug import check_password_hash, generate_password_hash
from helpers import *
import config


app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = os.environ['MYSQL_DATABASE_HOST'] if 'MYSQL_DATABASE_HOST' in os.environ else config.MYSQL_DATABASE_HOST
app.config['MYSQL_DATABASE_PORT'] = os.environ['MYSQL_DATABASE_PORT'] if 'MYSQL_DATABASE_PORT' in os.environ else config.MYSQL_DATABASE_PORT
app.config['MYSQL_DATABASE_USER'] = os.environ['MYSQL_DATABASE_USER'] if 'MYSQL_DATABASE_USER' in os.environ else config.MYSQL_DATABASE_USER
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ['MYSQL_DATABASE_PASSWORD'] if 'MYSQL_DATABASE_PASSWORD' in os.environ else config.MYSQL_DATABASE_PASSWORD
app.config['MYSQL_DATABASE_DB'] = os.environ['MYSQL_DATABASE_DB'] if 'MYSQL_DATABASE_DB' in os.environ else config.MYSQL_DATABASE_DB

mysql.init_app(app)

if 'SECRET_KEY' in os.environ: app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
else: app.config['SECRET_KEY'] = os.urandom(24)

def connect_db(): return mysql.connect()

def check_auth():
    g.user = None
    if 'username' in session:
        g.user = get_user(session['username'])
        return
    return redirect(url_for('login'))

@app.route('/')
def home(): 
    if 'username' in session: return redirect(url_for('main'))
    return render_template('home.html')

def connect_db(): return mysql.connect()

@app.teardown_request
def teardown_request(exception):
    if exception: print exception
    g.db.close()

@app.before_request
def before_request():
    print session.keys(), session.values()
    print("before request")
    print ('username' in session, "in session?")
    g.db = connect_db()
    g.user = None
    if "username" in session:
        g.user = get_user(session['username'])

@app.route('/login/', methods=['GET', 'POST'])
def login():
    """Logs the user in."""
    if 'username' in session:
        return redirect(url_for('main'))

    error = None
    if request.method == 'POST':
        print("login hit")
        user = get_user(request.form['username'])
        if user is None:
            error = 'Invalid username'
            print error
        elif not check_password_hash(user.password, request.form['password']):
            error = 'Invalid password'
            print error
        else:
            flash('You were logged in')
            print "logged in"
            session['username'] = request.form['username']
            g.user = request.form['username']
            print error, "error"
            return redirect(url_for('main'))

    return render_template('login.html', error=error)


@app.route('/about/')
def about(): return render_template('about.html')

@app.route('/logout')
def logout():
    check_auth()
    """Logs the user out."""
    session.pop('username', None)
    flash('You were logged out')
    return redirect(url_for('home'))

@app.route('/profile/', methods=['GET', 'POST'])
def profile():
    check_auth()
    g.user = get_user(session['username'])
    g.user.img = gravatar_url(g.user.email, 140)
    follower_count, followee_count = get_follower_info()
    return render_template('profile.html', user=g.user, followercount = follower_count, followeecount = followee_count)

@app.route('/favorites/', methods=['GET', 'POST'])
def favorites():
    print "in favorites"
    check_auth()
    tweets, g.user = get_faves()
    g.user.img = gravatar_url(g.user.email, 140)
    follower_count, followee_count = get_follower_info()
    print "in favorites"
    return render_template('favorites.html', user=g.user, tweets=tweets, followercount = follower_count, followeecount = followee_count)

@app.route('/edit/', methods=['GET', 'POST'])
def edit_profile():
    check_auth()

    g.user = get_user(session['username'])

    if request.method == 'POST':
        print "in edit profile post"
        update_user(request.form, session['username'])
        return redirect(url_for('profile'))

    g.user = get_user(session['username'])
    g.user.img = gravatar_url(g.user.email,140)
    follower_count, followee_count = get_follower_info()

    return render_template('edit_profile.html', user=g.user, followercount = follower_count, followeecount = followee_count)

@app.route('/main/')
def main(): 
    check_auth()
    print "Checked auth"
    tweets, user = get_main()
    g.user = user
    follower_count, followee_count = get_follower_info()
    return render_template('main.html', user=user, tweets=tweets, followercount = follower_count, followeecount = followee_count)

@app.route('/action/', methods=['GET', 'POST'])
def action():
    check_auth()
    print "ACTION"
    print request.form
    g.user = get_user(session['username'])
    print "user..."
    if request.method == 'POST':
        print "in post.."
        if 'Like' in request.form:
            print "in like.."
            like(g.user.username, request.form['tweetid'])
            print "liked"
            return redirect(url_for('main'))
        if 'Fav' in request.form:
            print "favoriting"
            favorite(g.user.username, request.form['tweetid'])
            print "favorited"
            return redirect(url_for('favorites'))
        if 'RT' in request.form:
            print "in retweet"
            retweet(g.user.username, request.form['tweetid'])
            create_tweet(request.form['content'])
            print "retweeted"
            return redirect(url_for('main'))
        print "i found nothing..."
    return redirect(url_for('main'))


@app.route('/userdata/', methods=['GET', 'POST'])
def user_data():
    print "ok"
    username = request.form['username']
    print username
    user = get_user_json(username)
    img, first, last, username, web, blurb = user['IMG'], user['First'], user['Last'], username, user['Web'], user['Blurb']
    if user is not None:
        return jsonify(img=img, first=first, last=last, username=username, web=web, blurb=blurb)
    return None

@app.route('/people/', methods=['GET', 'POST'])
def find_people(): #get's newest users 
    check_auth()
    if request.method == 'POST':
        print request.form
        users = search_people(request.form['username'])
        for u in users: u['IMG'] = gravatar_url(u['Email'], 40)
    else:         
        users = get_people_to_follow()
        for u in users: u['IMG'] = gravatar_url(u['Email'], 40)

    return render_template('find_people.html', users=users, user=g.user)

@app.route('/tags/', methods=['GET', 'POST'])
def find_tags():
    check_auth()
    if request.method == "GET":
        print "getting tags"
        tags = get_top_ten_recent_tags()
        for u in tags: u['IMG'] = gravatar_url(u['Email'], 40)
    else:
        print "finding tags"
        print request.form
        tags = get_tags(request.form['tagname'])
        for u in tags: u['IMG'] = gravatar_url(u['Email'], 40)

    return render_template('tags.html', tags=tags, user=g.user)

@app.route('/followers/', methods=['GET', 'POST'])
def followers():
    check_auth()
    followers = get_followers()
    g.user.img = gravatar_url(g.user.email, 140)
    follower_count, followee_count = get_follower_info()
    return render_template('followers.html', followers=followers, user=g.user, followercount = follower_count, followeecount = followee_count)

@app.route('/followees/', methods=['GET', 'POST'])
def followees():
    check_auth()
    followees = get_followees()
    g.user.img = gravatar_url(g.user.email, 140)
    follower_count, followee_count = get_follower_info()
    return render_template('followees.html', followees=followees, user=g.user, followercount = follower_count, followeecount = followee_count)

@app.route('/follow/', methods=['GET', 'POST'])
def follow():
    check_auth()
    follow_user(g.user.username, request.form['Username'])
    return redirect(url_for('followees'))

@app.route('/unfollow/', methods=['GET', 'POST'])
def unfollow():
    check_auth()
    unfollow_user(request.form['Username'], g.user.username)
    return redirect(url_for('followees'))

@app.route('/tweet/', methods=['GET', 'POST'])
def tweet():
    check_auth()
    if request.method == "POST": create_tweet(request.form['tweet'])
    return redirect(url_for('main'))

@app.route('/register/', methods=['GET', 'POST'])
def register():
    check_auth()
    error = None
    if request.method == 'POST':
        if not request.form['username']:
            error = 'You have to enter a username'
        elif not request.form['email'] or \
                 '@' not in request.form['email']:
            error = 'You have to enter a valid email address'
        elif not request.form['password']:
            error = 'You have to enter a password'
        elif get_user(request.form['username']) is not None:
            error = 'The username is already taken'
        else:
            user = add_user(request.form['username'],
                            request.form['email'],
                            generate_password_hash(request.form['password']))

            session['username'] = request.form['username']
            flash('You were successfully registered')
            return redirect(url_for('edit_profile'))
    return render_template('register.html', error=error)

###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)





