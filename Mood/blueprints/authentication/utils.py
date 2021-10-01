from flask import g, session, flash, redirect, url_for, abort
from functools import wraps
from Mood import db, bcrypt
from Mood.models import User


def login_user(user_id: int, remember: bool = False) -> None:
    """
        Authenticating a user...
        :params user_id: Queried User id
        :params remember: Save Session (365 days)
    """

    # Clear any Existing Sessions
    session.clear()
    # Assign Values to session
    session['is_authenticated'] = True
    session['user_id'] = user_id
    # Set The Cookies Life Time To 1 Year
    if remember:
        session.permanent = True


def register_user(uname: str, given_email: str, given_pwd: str, role: str = 'student') -> None:
    """
        Saving a New User To the DB
        :params uname: the Username
        :params given_email: Email @
        :params given_pwd: Password to be hashed
        :params given_email: role - by default == student
    """
    # hash given password
    hashed_password = bcrypt.generate_password_hash(given_pwd).decode('utf-8')
    # create a User instance
    user = User(username=uname, email=given_email, password=hashed_password, role=role)
    # Insert new user to the database
    db.session.add(user)
    db.session.commit()


def logout_user() -> None:
    """
        Clear Sessions
    """
    session.pop('user_id')
    session.pop('is_authenticated')
    session.clear()


def login_required(f):
    """ 
        Is the user accessing this page authenticated ??
        :params f: view function
        :return: Function
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'is_authenticated' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'red darken-3')
            return redirect(url_for('auth.login'))
    return wrap


def role_required(*roles):
    """ 
        Does a user have a authorization to access this page??
        :params *roles: 1 or more allowed roles
        :return: Function
    """
    def decorator(f):
        """
            :params f: view function
        """
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if g.current_user.role not in roles:
                abort(403)  # errorHandler : error_403
            return f(*args, **kwargs)
        return decorated_function
    return decorator
