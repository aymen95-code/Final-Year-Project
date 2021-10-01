from flask import Blueprint, render_template, redirect, url_for, flash
from Mood.blueprints.authentication.forms import RegistrationForm
from Mood.blueprints.authentication.utils import login_required, role_required, register_user
from Mood.models import User, Publication, ClassRoom
admin = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates')


@admin.before_request
@login_required
@role_required('admin')
def before_admin_request():
    """ Protect all the admin endpoints """
    pass


@admin.route('/')
def dashboard():
    num_of_users = User.query.count()
    num_of_pubs = Publication.query.count()
    num_of_classrooms = ClassRoom.query.count()
    return render_template('admin/stats.html', title='Current Website Statistics', num_of_users=num_of_users, num_of_pubs=num_of_pubs, num_of_classrooms=num_of_classrooms, dashboard=True)


@admin.route('/students')
def students():
    list_of_students = User.query.filter_by(role='student').all()
    return render_template('admin/students.html', title='students management', list_of_students=list_of_students, dashboard=True)


@admin.route('/professors', methods=['GET', 'POST'])
def teachers():
    list_of_teachers = User.query.filter_by(role='teacher').all()
    form = RegistrationForm()
    if form.validate_on_submit():
        register_user(form.username.data, form.email.data, form.password.data, 'teacher')
        flash('Professor Added Successfully')
        return redirect(url_for('admin.teachers'))
    return render_template('admin/teachers.html', title='teachers management', form=form, list_of_teachers=list_of_teachers, dashboard=True)


@admin.route('/settings')
def settings():
    return render_template('admin/settings.html', title='settings', dashboard=True)
