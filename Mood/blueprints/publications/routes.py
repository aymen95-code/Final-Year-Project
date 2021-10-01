from flask import (
        g,
        render_template,
        request,
        Blueprint,
        redirect,
        url_for,
        abort,
        flash
    )
from Mood import db
from Mood.models import Publication
from Mood.blueprints.publications.forms import CreatePubForm
from Mood.blueprints.authentication.utils import login_required

pubs = Blueprint('pubs', __name__, url_prefix='/pubs', template_folder='templates')


@pubs.before_request
@login_required
def check_anonymous_users():
    """ 
      This function will run before every request within the scope
      of the blueprint
      --> Protect all pubs endpoints from anonymous users
    """
    pass


@pubs.route('/all', methods=['GET', 'POST'])
def all_pubs():
    form = CreatePubForm()
    if form.validate_on_submit():
        pub = Publication(body=form.body.data, author=g.current_user)
        db.session.add(pub)
        db.session.commit()
        flash('Pub created successfully', 'teal darken-3')
        return redirect(url_for('pubs.get_pub', pub_id=pub.id))
    list_of_pubs = Publication.query.order_by(Publication.date_posted.desc()).all()
    return render_template('publications/all.html', form=form, title="Discussions", pubs=list_of_pubs)


@pubs.route('/<int:pub_id>')
def get_pub(pub_id):
    """
        A view func that looks for a specific publication in the database and return it back,
        In case the publication does not exist, it will raise a 404 HTTP Response
        :params pub_id: the specific publication Id of type Integer
    """
    pub = Publication.query.filter_by(id=pub_id).first_or_404()
    return render_template('publications/pub.html', pub=pub)


@pubs.route('/<int:pub_id>/update', methods=['GET', 'POST'])
def update_pub(pub_id):
    pub = Publication.query.filter_by(id=pub_id).first_or_404()
    form = CreatePubForm()
    if form.validate_on_submit():
        pub.body = form.body.data
        db.session.commit()
        flash('Pub Updated With Success', 'teal darken-3')
        return redirect(url_for('pubs.get_pub', pub_id=pub.id))
    form.body.data = pub.body
    return render_template('publications/updatePub.html', pub=pub, form=form, title="Update Pub")


@pubs.route('/<int:pub_id>/delete', methods=['POST'])
def delete_pub(pub_id):
    pub = Publication.query.get_or_404(pub_id)
    if pub.author != g.current_user:
        abort(403)
    db.session.delete(pub)
    db.session.commit()
    flash('Pub was removed successfully', 'teal darken-3')
    return redirect(url_for('pubs.all_pubs'))


@pubs.route('/<int:pub_id>/actions/<string:action>')
def pub_reaction(pub_id, action):
    pub = Publication.query.get_or_404(pub_id)
    if action == 'like':
        g.current_user.like_post(pub)
        db.session.commit()
    elif action == 'dislike':
        g.current_user.unlike_post(pub)
        db.session.commit()
    return redirect(request.referrer)

