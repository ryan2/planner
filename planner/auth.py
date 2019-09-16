import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from planner.db import get_db
from bson.objectid import ObjectId

bp = Blueprint('auth',__name__, url_prefix='/auth')

@bp.route('/register', methods = ('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        mongo = get_db()
        error = None

        if not username:
            error = 'Username is Required!'
        elif not password:
            error = 'Password is Required!'
        elif mongo.db.users.find_one({"username":username}) is not None:
            error = 'Username {} is taken!'.format(username)
        
        if error is None:
            mongo.db.users.insert_one({"username":username, "password":generate_password_hash(password)})
            return redirect(url_for('auth.login'))

        flash(error)
    return render_template('auth/register.html')

@bp.route('/login', methods = ('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        mongo = get_db()
        error = None
        user = mongo.db.users.find_one({"username":username})
        if user is None or not check_password_hash(user['password'],password):
            error = 'Invalid Username and Password combination'

        if error is None:
            session.clear()
            session['user_id'] = user['_id']
            return redirect(url_for('index'))
        
        flash(error)
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = ObjectId(session.get('user_id'))
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().db.users.find_one({'_id':user_id})

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
