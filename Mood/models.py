from datetime import datetime
from Mood import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(6), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_online = db.Column(db.DateTime, default=datetime.utcnow)
    profile_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    role = db.Column(db.String(24), default='student')
    publications = db.relationship('Publication', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='commentator', lazy='dynamic')
    class_room_head = db.relationship('ClassRoom', backref='head', lazy='dynamic')
    # likes relationship
    liked = db.relationship('PublicationLike', foreign_keys='PublicationLike.user_id', backref='user', lazy='dynamic')
    # Class Rooms member relationship
    class_member = db.relationship('ClassRoomMember', foreign_keys='ClassRoomMember.user_id', backref='member', lazy='dynamic')

    """ Likes Methods """

    def like_post(self, post):
        if not self.has_liked_post(post):
            like = PublicationLike(user_id=self.id, pub_id=post.id)
            db.session.add(like)

    def unlike_post(self, post):
        if self.has_liked_post(post):
            PublicationLike.query.filter_by(
                user_id=self.id,
                pub_id=post.id).delete()

    def has_liked_post(self, post):
        return PublicationLike.query.filter(
            PublicationLike.user_id == self.id,
            PublicationLike.pub_id == post.id).count() > 0

    """ Class Room Methods """

    def join_class(self, classroom):
        if not self.is_class_member(classroom):
            member = ClassRoomMember(user_id=self.id, class_room_id=classroom.id)
            db.session.add(member)

    def leave_class(self, classroom):
        if self.is_class_member(classroom):
            ClassRoomMember.query.filter_by(
                user_id=self.id,
                class_room_id=classroom.id
            ).delete()

    def is_class_member(self, classroom):
        return ClassRoomMember.query.filter(
            ClassRoomMember.user_id == self.id,
            ClassRoomMember.class_room_id == classroom.id
        ).count() > 0

    def __repr__(self):
        return f'<User : {self.id}, {self.email}, {self.username}, {self.date_joined}'


# N*N
class PublicationLike(db.Model):
    __tablename__ = 'pub_like'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pub_id = db.Column(db.Integer, db.ForeignKey('publications.id'))


class Publication(db.Model):
    __tablename__ = "publications"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime,
                            nullable=False,
                            default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='publication', lazy='dynamic')
    likes = db.relationship('PublicationLike', backref='publication', lazy='dynamic')

    def __repr__(self):
        return f'<Publication : {self.id}, {self.title}, {self.date_posted}'


# N*N
class ClassRoomMember(db.Model):
    __tablename__ = "class_members"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    class_room_id = db.Column(db.Integer, db.ForeignKey('classrooms.id'))


class ClassRoom(db.Model):
    __tablename__ = "classrooms"
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(60), nullable=False)
    description = db.Column(db.Text, nullable=False)
    cover_image = db.Column(db.String(20), nullable=False, default='default_class_cover.jpg')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    professor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    members = db.relationship('ClassRoomMember', backref='classroom', lazy='dynamic')

    def __repr__(self):
        return f'<ClassRoom : {self.id} taught by {self.professor_id}'


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime,
                            nullable=False,
                            default=datetime.utcnow)
    author = db.Column(db.Integer, db.ForeignKey('users.id'))
    publication_id = db.Column(db.Integer, db.ForeignKey('publications.id'))

    def __repr__(self):
        return f'<Publication : {self.id}, {self.body}, {self.date_posted}'
