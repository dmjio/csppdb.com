import os
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, _app_ctx_stack
from flaskext.mysql import MySQL
from contextlib import closing
from datetime import datetime
from helpers import *
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

def connect_db(): return mysql.connect()

@app.before_request
def before_request():
    g.db = connect_db()
    g.user = None
    if 'userid' in session: g.user = get_user_by_id(g, session['userid'])

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.route('/about/') 
def about(): return render_template('about.html')

@app.route('/logout')
def logout():
    """Logs the user out."""
    g.user = None
    session.pop('userid', None)
    flash('You were logged out')
    return redirect(url_for('home'))

@app.route('/profile/', methods=['GET', 'POST'])
def profile():
    user = get_user_by_id(g, g.user.user_id)
    user.img = gravatar_url(user.email,140)
    return render_template('profile.html', user=user)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    """Logs the user in."""
    if g.user: return redirect(url_for('main'))
    error = None
    if request.method == 'POST':
        user = get_user(g, request.form['username'])
        if user is None:
            error = 'Invalid username'
        elif not check_password_hash(user.password, request.form['password']):
            error = 'Invalid password'
        else:
            flash('You were logged in')
            g.user = user
            session['userid'] = user.user_id
            return redirect(url_for('main'))
    return render_template('login.html', error=error)


@app.route('/main/', methods=['GET', 'POST'])
def main():
    if 'userid' not in session or not g.user or session['userid'] is None:
        return redirect(url_for('login'))
    else:
        sql = "select t.*, u.img, u.username, u.email from tweets t inner join users u on t.userid = u.userid;"
        tweets = get_data(g, sql)

        for i in tweets:
            i['img'] = gravatar_url(i['email'], 30)

        g.user.img = gravatar_url(g.user.email, 140)
        return render_template('main.html', user=g.user, tweets=tweets)

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if g.user:
        return redirect(url_for('main'))
    error = None
    if request.method == 'POST':
        if not request.form['username']:
            error = 'You have to enter a username'
        elif not request.form['email'] or \
                 '@' not in request.form['email']:
            error = 'You have to enter a valid email address'
        elif not request.form['password']:
            error = 'You have to enter a password'
        elif get_user(g, request.form['username']) is not None:
            error = 'The username is already taken'
        else:
            username = request.form['username']
            email = request.form['email']
            password = generate_password_hash(request.form['password'])

            username = stringify(username)
            email = stringify(email)
            password = stringify(password)

            sql = "insert into users (username, email, password) values (%s, %s, %s)" % (username, email, password,)
            cursor = g.db.cursor()
            cursor.execute(sql)
            g.db.commit()

            g.user = get_user(g, request.form['username'])
            session['userid'] = g.user.user_id

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





