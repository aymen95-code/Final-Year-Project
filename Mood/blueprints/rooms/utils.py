import random
import string
from flask import g
from Mood import db
from Mood.models import ClassRoom
from Mood.blueprints.accounts.utils import save_pic


def add_classroom(name: str, description: str, cover_image) -> None:
    cover_image_saved = save_pic(cover_image, 'static/cover_pics')
    classroom = ClassRoom(
            class_name=name,
            description=description,
            cover_image=cover_image_saved,
            head=g.current_user
        )
    # the teacher joins automatically
    g.current_user.join_class(classroom)
    db.session.commit()
    # add class room to the database
    db.session.add(classroom)


def get_random_string(length: int = 16) -> str:
    """ get_random_string(16) """
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str