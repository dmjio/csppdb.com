from flask.ext.login import *
import os
from flask import Flask, request, session, url_for, redirect, \
     render_template, g, flash
from flaskext.mysql import MySQL
from data import *
from werkzeug import check_password_hash, generate_password_hash
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

###
# Routing for your application.
###

login_manager = LoginManager()
login_manager.refresh_view = "reauth"
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(username):
    g.db = connect_db()
    return get_user(username)

login_manager.init_app(app)

@app.route('/')
def home(): return render_template('home.html')

@app.route('/about/') 
def about(): return render_template('about.html')

def connect_db(): return mysql.connect()

@app.route('/logout')
@login_required
def logout():
    """Logs the user out."""
    logout_user()
    flash('You were logged out')
    return redirect(url_for('home'))

@app.before_request
def before_request():
    g.user = current_user
    g.db = connect_db()

@app.teardown_request
def tear_down(exception):
    g.db.close()

@app.route("/reauth", methods=["GET", "POST"])
@login_required
def reauth():
    if request.method == "POST":
        confirm_login()
        flash(u"Reauthenticated.")
        return redirect(request.args.get("next") or url_for("main"))
    return render_template("login.html")

@app.route('/profile/', methods=['GET', 'POST'])
@login_required
def profile():
    user = get_user(g.user.username)
    user.img = gravatar_url(user.email,140)
    return render_template('profile.html', user=user)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    """Logs the user in."""
    if request.method == 'GET':
        if current_user is user_logged_in: logout_user()

    error = None
    if request.method == 'POST':
        user = get_user(request.form['username'])
        if user is None:
            error = 'Invalid username'
        elif not check_password_hash(user.password, request.form['password']):
            error = 'Invalid password'
        else:
            flash('You were logged in')
            login_user(user)
            return redirect(url_for('main'))

    return render_template('login.html', error=error)

@app.route('/main/')
@login_required
def main():
    tweets, user = get_main()
    follower_count, followee_count = get_follower_info(g.user.username)
    return render_template('main.html', user=user, tweets=tweets, followercount = follower_count, followeecount = followee_count)

@app.route('/people/', methods=['GET', 'POST'])
@fresh_login_required
def find_people():
    users = get_people_to_follow(g.user.username)
    for u in users: u['IMG'] = gravatar_url(u['Email'], 40)
    return render_template('find_people.html', users=users, user=g.user)

@app.route('/tags/', methods=['GET', 'POST'])
@fresh_login_required
def find_tags():
    if request.method == "GET":
        tags = get_top_ten_recent_tags()
    else:
        tags = get_tags()
        for u in tags: u['IMG'] = gravatar_url(u['Email'], 40)

    return render_template('tags.html', tags=tags, user=g.user)

@app.route('/followers/', methods=['GET', 'POST'])
@login_required
def followers():
    followers = get_followers(g.user.username)
    user = get_user(g.user.username)
    user.img = gravatar_url(user.email, 140)
    follower_count, followee_count = get_follower_info(g.user.username)
    return render_template('followers.html', followers=followers, user=user, followercount = follower_count, followeecount = followee_count)

@app.route('/followees/', methods=['GET', 'POST'])
@login_required
def followees():
    followees = get_followees(g.user.username)
    user = get_user(g.user.username)
    user.img = gravatar_url(user.email, 140)
    follower_count, followee_count = get_follower_info(g.user.username)
    return render_template('followees.html', followees=followees, user=user, followercount = follower_count, followeecount = followee_count)

@app.route('/follow/', methods=['GET', 'POST'])
@login_required
def follow():
    follow_user(g.user.username, request.form['Username'])
    return redirect(url_for('main'))

@app.route('/unfollow/', methods=['GET', 'POST'])
@login_required
def unfollow():
    unfollow_user(request.form['Username'], g.user.username)
    return redirect(url_for('followees'))

@app.route('/tweet/', methods=['GET', 'POST'])
@login_required
def tweet():
    if request.method == "POST": create_tweet(request.form['tweet'])
    return redirect(url_for('main'))


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        if current_user is user_logged_in: logout_user()
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

            login_user(user)
            flash('You were successfully registered')
            return redirect(url_for('main'))
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
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)





