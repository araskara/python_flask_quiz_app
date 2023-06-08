from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, QuForm, ChoiceForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = '83C551DCFC2BAB5671487DADAF8CB'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ---------- Model ---------------

'''class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
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

    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class ChoiceAn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(20), nullable=False )
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)




# ---------- End Model---------------


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Welcome')


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/login')
def login():
    return render_template('login.html', title='Login', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/quiz')
def quiz():
    quizzes = Post.query.all()
    return render_template('quizz.html', quizzes=quizzes, title='Quiz')


@app.route('/qu', methods=['GET', 'POST'])
def qu():
    form = QuForm()
    if form.validate_on_submit():
        quizzes = Post(title=form.title.data, content=form.content.data,
                       option1=form.option1.data,
                       option2=form.option2.data,
                       option3=form.option3.data,
                       option4=form.option4.data,
                       optionCorrect=form.optionCorrect.data)

        db.session.add(quizzes)
        db.session.commit()
        flash('Quiz has been created!', 'success')
        return redirect(url_for('quiz'))
    return render_template('qu.html', title='Add Quiz',
                           form=form, legend='New Post')


@app.route('/quiz/<int:post_id>/update', methods=['GET', 'POST'])
def update_quiz(post_id):
    quizzes = Post.query.get_or_404(post_id)
    form = QuForm()
    if form.validate_on_submit():
        quizzes.title = form.title.data
        quizzes.content = form.content.data
        quizzes.option1 = form.option1.data
        quizzes.option2 = form.option2.data
        quizzes.option3 = form.option3.data
        quizzes.option4 = form.option4.data
        db.session.commit()
        flash('Quiz has been updated!', 'success')
        return redirect(url_for('quiz'))
    elif request.method == 'GET':
        form.title.data = quizzes.title
        form.content.data = quizzes.content
        form.option1.data = quizzes.option1
        form.option2.data = quizzes.option2
        form.option3.data = quizzes.option3
        form.option4.data = quizzes.option4

    return render_template('qu.html', title='Update Qu',
                           form=form, legend='Update Post')


@app.route('/quiz/<int:post_id>/delete', methods=['GET', 'POST'])
def delete_quiz(post_id):
    quizzes = Post.query.get_or_404(post_id)
    db.session.delete(quizzes)
    db.session.commit()
    flash('Quiz has been deleted!', 'success')
    return redirect(url_for('quiz'))


@app.route('/quiz/<int:post_id>/answer', methods=['POST'])
def choice(post_id):
    radio = request.form.get('exampleRadios')
    choiceAn = ChoiceAn(answer=radio, post_id=post_id)
    db.session.add(choiceAn)
    db.session.commit()
    return redirect(url_for('quiz'))






'''
def choice(post_id):
    answer = Post.query.get_or_404(post_id)
    form = ChoiceForm()
    if form.validate_on_submit():
        answer = Choice(choice=form.choice.data)
    db.session.add(answer)
    db.session.commit()
    flash('Answer submitted', 'success')
    return redirect(url_for('quiz'))
'''

if __name__ == '__main__':
    app.run()
