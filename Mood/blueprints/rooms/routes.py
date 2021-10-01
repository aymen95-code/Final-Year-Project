from flask import (
    g,
    Blueprint,
    render_template,
    redirect,
    request,
    url_for,
    flash,
    abort
)
from Mood import db
from Mood.models import ClassRoom, ClassRoomMember, User
from Mood.blueprints.authentication.utils import login_required, role_required
from Mood.blueprints.rooms.forms import AddClassRoomForm, AddMembersForm
from Mood.blueprints.rooms.utils import add_classroom, get_random_string

room = Blueprint('room', __name__, url_prefix='/room', template_folder='templates')


@room.before_request
@login_required
def check_anonymous_users():
    pass


@room.route('/')
def videoroom():
    return render_template('room/room.html', title='Online Lecture')


@room.route('/classes', methods=['GET', 'POST'])
def get_classes():
    classes = ClassRoom.query.all()
    return render_template('room/classes.html',
                           title='Available Classes',
                           classes=classes)


@room.route('/classes/add', methods=['GET', 'POST'])
@role_required('teacher')
def add_class_room():
    form = AddClassRoomForm()
    if form.validate_on_submit():
        add_classroom(form.name.data, form.description.data, form.cover_file.data)
        db.session.commit()
        return redirect(url_for('room.get_classes'))
    return render_template('room/addClass.html',
                            title='Add Classroom',
                            form = form)


@room.route('/<int:cls_id>', methods=['GET', 'POST'])
def get_clsroom(cls_id):
    cls_room = ClassRoom.query.get_or_404(cls_id)
    if not g.current_user.is_class_member(cls_room):
        abort(403)
    
    form = AddMembersForm()
    if form.validate_on_submit():
        new_member = User.query.filter_by(username=form.username.data).first()
        new_member.join_class(cls_room)
        db.session.commit()
        flash('user was added successfully', 'teal darken-1')
        return redirect(url_for('room.get_clsroom', cls_id=cls_room.id))
    return render_template('room/class.html', title=cls_room.class_name, form=form, cls_room=cls_room)


@room.route('/class/<int:cls_id>/<string:action>')
def classroom_actions(cls_id, action):
    cls_room = ClassRoom.query.get_or_404(cls_id)
    if action == 'join':
        g.current_user.join_class(cls_room)
        db.session.commit()
        flash(f'You have joined {cls_room.class_name} succussefully', 'teal darken-1')
        return redirect(url_for('room.get_clsroom', cls_id=cls_room.id))
    elif action == 'leave':
        g.current_user.leave_class(cls_room)
        db.session.commit()
        flash(f'You have left {cls_room.class_name} succussefully', 'red darken-1')
        return redirect(url_for('room.get_classes'))
