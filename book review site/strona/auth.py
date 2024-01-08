from functools import wraps
from flask import session, redirect, url_for
from db_utils import fetch_user


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        username = session.get('username')
        if username:
            user_data = fetch_user(username)
            if user_data['admin'] == 1:
                return f(*args, **kwargs)
        return 'forbidden'

    return decorated_function
