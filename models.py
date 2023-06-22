from datetime import datetime
from init import db, login_manager
from flask_login import UserMixin



@login_manager.user_loader
def load_user(user_id):
    return  User.query.get(int(user_id))


# ---------- Model ---------------

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

'''
class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    questions = db.relationship('Post', backref='quiz', lazy=True)

'''

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.String(300), nullable=False)
    option2 = db.Column(db.String(300), nullable=False)
    option3 = db.Column(db.String(300), nullable=False)
    option4 = db.Column(db.String(300), nullable=False)
    optionCorrect = db.Column(db.String(300), nullable=False)
    choiceAn = db.relationship('ChoiceAn', passive_deletes=True)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class ChoiceAn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(20), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)


# ---------- End Model---------------