from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from config import SQLALCHEMY_DATABASE_URI

db = SQLAlchemy()

relationship_table = db.Table('relationship_table',                            
        db.Column('user_id', db.Integer,db.ForeignKey('users.id'), nullable=False),
        db.Column('post_id',db.Integer,db.ForeignKey('posts.id'), nullable=False),
        db.PrimaryKeyConstraint('user_id', 'post_id'))

class Users(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(255),nullable=False)
        posts = db.relationship('Posts', secondary=relationship_table, backref='users')  

        def __init__(self, name=None):
            self.name = name

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    string = db.Column(db.String, nullable=False)

    def __init__(self, name=None, string=None):
        self.name = name
        self.string = string


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.test_request_context():
        db.create_all()
    return app

def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance
        
def register_event(user, post_id, string):
    post = get_post(post_id)
    new_post = Posts(post_id, string)

    if post == None: # new post
        user.posts.append(new_post)
        db.session.commit()
    elif user not in post.users: # old post, new user
        user.posts.append(post)
        db.session.commit()

    return (post == None) or (user not in post.users)

def get_post(name):
    return Posts.query.filter(Posts.name == name).first()

def get_db_user(name):
    return get_or_create(db.session, Users, name=name)
