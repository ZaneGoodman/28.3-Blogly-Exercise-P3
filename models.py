from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(50), nullable=False, unique=True)

    last_name = db.Column(db.String(50), nullable=False)

    img_url = db.Column(db.Text)


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(50), nullable=False)

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.now)

    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    tags = db.relationship("Tag", secondary="posts_tags", backref="posts")

    user = db.relationship("User", backref="posts")


class Tag(db.Model):
    __tablename__ = "tags"

    tag_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    tag_name = db.Column(db.String(15), nullable=False, unique=True)


class PostTag(db.Model):
    __tablename__ = "posts_tags"

    post_id = db.Column(
        db.Integer, db.ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True
    )

    tag_id = db.Column(
        db.Integer, db.ForeignKey("tags.tag_id", ondelete="CASCADE"), primary_key=True
    )
