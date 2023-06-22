from init import db, login_manager
from flask import Flask, render_template, url_for, flash, redirect, request
from models import User, Post, ChoiceAn
from forms import RegistrationForm, QuForm, LoginForm,QuizCreationForm
from flask_bcrypt import Bcrypt
from flask_login import login_user, logout_user, current_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = '83C551DCFC2BAB5671487DADAF8CB'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db.init_app(app)
login_manager.init_app(app)

with app.app_context():
    db.create_all()

bcrypt = Bcrypt(app)


# ---------- URL & View---------------

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Welcome')


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


'''
@app.route('/create_quiz', methods=['GET', 'POST'])
@login_required
def create_quiz():
    form = QuizCreationForm() # assuming you have a QuizCreationForm
    if form.validate_on_submit():
        new_quiz = Quiz(title=form.title.data, description=form.description.data, author=current_user)
        db.session.add(new_quiz)
        db.session.commit()
        flash('Your quiz has been created!', 'success')
        return redirect(url_for('home')) # or wherever you want to go after creating a quiz
    return render_template('create_quiz.html', title='Create Quiz', form=form)

'''



@app.route('/quiz')
def quiz():
    quizzes = Post.query.all()
    return render_template('quizz.html', quizzes=quizzes, title='Quiz')


@app.route('/qu', methods=['GET', 'POST'])
@login_required
def question():
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
    return render_template('qu.html', title='Add Question',
                           form=form, legend='New Question')


@app.route('/quiz/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
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
@login_required
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


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


# ---------- End URL & View---------------


if __name__ == '__main__':
    app.run()
