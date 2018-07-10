import models
import forms

from flask import (Flask, render_template, flash, redirect, url_for,
                   g)
from resources.todos import todos_api
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user,
                         logout_user, login_required, current_user)

import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.register_blueprint(todos_api)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database before each request"""
    # g is used globally so we attach thing to access them everywhere
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """Close the db after each request"""
    g.db.close()
    return response


@app.route('/')
@login_required
def my_todos():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
            print('try')
        except models.DoesNotExist:
            flash("Your email or password doesn't match", "error")
            print('except')
        else:
            print('else')
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've been logged in!", "Success")
                return redirect(url_for('my_todos'))
            else:
                flash("Your email or password doesn't match", "error")
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegisterForm()
    # let's check those validators
    if form.validate_on_submit():
        flash('Yay, you registered', 'success')
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for('my_todos'))
    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out!")
    return redirect(url_for('login'))


if __name__ == '__main__':
    models.initialize()
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)
