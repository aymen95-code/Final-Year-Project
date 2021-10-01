# access db :
    - psql -U aymen -d mood

# Creating an admin
    - open flask shell
    - import db, bcrypt from Mood
    - import User from Mood.models
    - Create a user instance
        admin = User(username='admin', email='admin@mood.com', password=bcrypt.generate_password_hash('admin').decode('utf-8'), role='admin')
    - Commiting to db
        db.session.add(admin)
        db.session.commit()

# Making Many-To-Many Relationship
    - Likes : https://stackoverflow.com/questions/52665707/how-do-i-implement-a-like-button-function-to-posts-in-python-flask
    - Classes : ###

# Flask Patterns:
    - https://flask.palletsprojects.com/en/1.1.x/patterns/

# Tuturial on sessions:
    - https://overiq.com/flask-101/sessions-in-flask/
