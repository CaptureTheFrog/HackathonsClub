from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required
from users.forms import LoginForm, UserRegistrationForm, SponsorRegistrationForm
from models.user import User
from app import db, app
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join(app.root_path, 'static/img/')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

users_blueprint = Blueprint('users', __name__, template_folder='templates', static_folder='static')


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if (not user
                or not user.verify_password(form.password.data)):
            flash('Invalid username or password')
            return render_template('users/login.html', form=form)
        login_user(user)
        # TODO: render appropriate page based on user role
        return redirect(url_for('index'))
    return render_template('users/login.html', form=form)


@users_blueprint.route('/logout')
@login_required
# @requires_roles('user', 'admin') TODO: CHANGE
def logout():
    # log out user
    logout_user()
    # redirect user to index page
    return redirect(url_for('index')) # TODO: change redirect


@users_blueprint.route('/profile')
@login_required
def profile():
    return render_template('users/profile.html') # TODO: replace with actual code


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_picture(form):
    if request.method == 'POST':
        # if user does not select file
        if 'picture' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['picture']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # use company name + extension as filename
            filename = secure_filename(form.company.data.lower() + '.' + file.filename.rsplit('.', 1)[1].lower())
            print(file)
            with open(app.config['UPLOAD_FOLDER'] + filename, 'wb') as f:
                f.write(file.read())


def register_user(form, role):
    # check if email already exists
    user = User.query.filter_by(email=form.email.data).first()
    if user:
        flash('Email address already exists.')
        return render_template('users/register.html', form=form)

    save_picture(form)

    new_user = User(email=form.email.data,
                    password=form.password.data,
                    role=role)
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)
    return redirect(url_for('index')) # TODO: remove?


@users_blueprint.route('/register/participant', methods=['GET', 'POST'])
def participant_registration():
    form = UserRegistrationForm()
    if form.validate_on_submit():
        register_user(form, 'participant')
        return redirect(url_for('index')) # TODO: change redirect
    return render_template('users/register.html', form=form, role='participant')


@users_blueprint.route('/register/organizer', methods=['GET', 'POST'])
def organizer_registration():
    form = UserRegistrationForm()
    if form.validate_on_submit():
        register_user(form, 'organizer')
        return redirect(url_for('index')) # TODO: change redirect
    return render_template('users/register.html', form=form, role='organizer')


@users_blueprint.route('/register/sponsor', methods=['GET', 'POST'])
def sponsor_registration():
    form = SponsorRegistrationForm()
    if form.validate_on_submit():
        register_user(form, 'sponsor')
        return redirect(url_for('index')) # TODO: change redirect
    return render_template('users/register.html', form=form, role='sponsor')


@users_blueprint.route('/role_selection')
def role_selection():
    return render_template('users/role_selection.html')