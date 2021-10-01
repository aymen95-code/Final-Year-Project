import os
import secrets
from flask import current_app

def save_pic(form_picture, folder_path:str) -> str:
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    # rename it
    picture_filename = random_hex + f_ext
    # path
    picture_path = os.path.join(current_app.root_path, folder_path, picture_filename)
    # save it
    form_picture.save(picture_path)
    # return filename
    return picture_filename