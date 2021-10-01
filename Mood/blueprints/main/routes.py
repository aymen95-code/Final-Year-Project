from flask import render_template, Blueprint
from Mood.models import Publication

main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
def index():
    pubs = Publication.query.order_by(Publication.date_posted.desc()).paginate(page=1, per_page=3)
    return render_template('main/index.html', title='Mood | Home', pubs=pubs)


@main.route('/live_video')
def live_video():
    return render_template('video.html')
