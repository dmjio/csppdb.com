import os
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, _app_ctx_stack
from flaskext.mysql import MySQL
from contextlib import closing
from hashlib import md5
from datetime import datetime
from helpers import *
from werkzeug import check_password_hash, generate_password_hash
import config


app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = config.MYSQL_DATABASE_HOST
app.config['MYSQL_DATABASE_PORT'] = config.MYSQL_DATABASE_PORT
app.config['MYSQL_DATABASE_USER'] = config.MYSQL_DATABASE_USER
app.config['MYSQL_DATABASE_PASSWORD'] = config.MYSQL_DATABASE_PASSWORD
app.config['MYSQL_DATABASE_DB'] = config.MYSQL_DATABASE_DB

mysql.init_app(app)

if 'SECRET_KEY' in os.environ: app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
else: app.config['SECRET_KEY'] = os.urandom(24)

###
# Routing for your application.
###


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('init.sql') as f:
            db.cursor().execute(f.read())
        db.commit()

def connect_db(): return mysql.connect()

@app.before_request
def before_request():
    g.user = None
    if 'userid' in session:
        g.user = get_user_by_id(g, session['userid'])


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


def format_datetime(timestamp):
    """Format a timestamp for display."""
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d @ %H:%M')

def gravatar_url(email, size=80):
    """Return the gravatar image for the given email address."""
    return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%d' % \
        (md5(email.strip().lower().encode('utf-8')).hexdigest(), size)

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
    session['userid'] = None
    flash('You were logged out')
    return redirect(url_for('home'))

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
    if not g.user or 'userid' not in session:
        return redirect(url_for('login'))
    else:
        return render_template('main.html')

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
        elif get_user_id(request.form['username']) is not None:
            error = 'The username is already taken'
        else:
            username = request.form['username']
            email = request.form['email']
            password = generate_password_hash(request.form['password'])

            username = stringify(username)
            email = stringify(email)
            password = stringify(password)

            g.db.cursor().execute("insert into users (username, email, password) values (%s, %s, %s)" % (username, email, password,))
            g.db.commit()

            g.user = get_user(g, username)
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

def get_user_id(username):
    """Convenience method to look up the id for a username."""
    sql = 'select * from Users where Username = %s' % stringify(username)
    cursor = g.db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result[0] if result else None


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
    init_db()



