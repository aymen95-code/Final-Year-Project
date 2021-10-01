from datetime import datetime
from flask import g, Blueprint, request, session, render_template, flash, redirect, url_for
from Mood import db, bcrypt
from Mood.blueprints.authentication.forms import LoginForm, RegistrationForm
from Mood.blueprints.authentication.utils import login_user, logout_user, register_user, login_required
from Mood.models import User

auth = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates')


@auth.before_app_request
def load_user():
    """
      This function will run before every request outside or within the scope
      of the blueprint
      --> Set the current user logged in as a global variable
    """
    user_id: int = session.get('user_id')
    g.current_user = None
    g.is_authenticated = False

    if user_id:
        g.current_user = User.query.filter_by(id=user_id).first()
        if g.current_user:
            # in case the account still exist
            g.is_authenticated = session.get('is_authenticated')


@auth.before_app_request
def set_last_online():
    """
      This function will run before every request outside or within the scope
      of the blueprint
      --> Update the last_online field with the last time the user was online
   """
    if g.is_authenticated:
        g.current_user.last_online = datetime.utcnow()
        db.session.commit()


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # if the user is already logged in, redirect to the home page
    is_authenticated = session.get('is_authenticated')
    if is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    # if req.method == POST
    if form.validate_on_submit():
        # Fetch the user from a database
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # the user exists and the password matched
            login_user(user.id, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Welcome Back {user.username}', 'teal darken-3')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash(f'Invalid Credentials. Please Try again...', 'red darken-3')
            return redirect(url_for('auth.login'))
    return render_template('auth/login.html', form=form, title="Login")


@auth.route('/register', methods=['GET', 'POST'])
def register():
    # if the user is already logged in, redirect to the home page
    is_authenticated = session.get('is_authenticated')
    if is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        register_user(form.username.data, form.email.data, form.password.data)
        # Successful registration
        flash('Your account was created Successfully, you can now login :)', 'teal darken-3')
        # redirect to the login view
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'teal darken-3')
    return redirect(url_for('auth.login'))
