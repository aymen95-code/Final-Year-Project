from flask import g, render_template, Blueprint, url_for, redirect, abort, flash
from Mood import db
from Mood.models import User, Publication
from Mood.blueprints.authentication.utils import login_required
from Mood.blueprints.accounts.forms import UpdateAccountForm
from Mood.blueprints.accounts.utils import save_pic

account = Blueprint('account', __name__, url_prefix='/user', template_folder='templates')


# Authentication Middleware
@account.before_request
@login_required
def check_anonymous_users():
    """ Protect all account endpoints from anonymous users """
    pass


@account.route('/<string:username>')
def user_account(username):
    user = User.query.filter_by(username=username).first_or_404()
    pubs = Publication.query.filter_by(author=user).order_by(Publication.date_posted.desc()).all()
    image_file = url_for('static', filename='profile_pics/' + user.profile_file)
    return render_template('accounts/profile.html', user=user, pubs=pubs, title=user.username + ' | Profile',
                           img=image_file)


@account.route('/<string:username>/update', methods=['GET', 'POST'])
def update_account(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user != g.current_user:
        abort(403)
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.profile_pic.data:
            pic_fn = save_pic(form.profile_pic.data, 'static/profile_pics')
            user.profile_file = pic_fn
        user.username = form.username.data
        user.email = form.email.data
        db.session.commit()
        flash('Your Account Has been updated', 'teal darken-3')
        return redirect(url_for('account.user_account', username=user.username))
    form.username.data = user.username
    form.email.data = user.email
    return render_template('accounts/updateProfile.html', form=form, title='Update Account')


@account.route('/<int:user_id>/delete', methods=['POST'])
def delete_account(user_id):
    user = User.query.get_or_404(user_id)
    if user != g.current_user:
        abort(403)
    db.session.delete(user)
    db.session.commit()
    flash(f'{user.username} Has been deleted', 'teal darken-3')
    return redirect(url_for('auth.logout'))
