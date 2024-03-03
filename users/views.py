from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from users.forms import LoginForm, UserRegistrationForm, SponsorRegistrationForm, PasswordForm
from models.user import User
from app import db, app
import os
from werkzeug.utils import secure_filename
from models.sponsor import Sponsor

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
def logout():
    # log out user
    logout_user()
    # redirect user to index page
    return redirect(url_for('index')) # TODO: change redirect


from utils.decorators import requires_roles

@users_blueprint.route('/profile')
@login_required
@requires_roles('participant', 'organizer', 'sponsor')
def profile():
    data = {}
    if current_user.role == 'sponsor':
        return render_template('users/profile.html',
                                prof_no=current_user.id,
                                email=current_user.email,
                                role=current_user.role,
                                company='placeholder', # TODO: get company info from sponsor table
                                phone='placeholder',
                                website='placeholder')
    elif current_user.role == 'participant' or current_user.role == 'organizer':
        return render_template('users/profile.html',
                                prof_no=current_user.id,
                                email=current_user.email,
                                role=current_user.role)

@users_blueprint.route('/update_password', methods=['GET', 'POST'])
@login_required
def update_password():
    form = PasswordForm()
    if form.validate_on_submit():
        if not current_user.verify_password(form.current_password.data):
            flash('Incorrect current password.')
            return render_template('users/update_password.html', form=form)

        if current_user.verify_password(form.new_password.data):
            flash('New password cannot be the same as the current password.')
            return render_template('users/update_password.html', form=form)

        current_user.password = form.new_password.data
        db.session.commit()
        flash('Password updated successfully.')
        return redirect(url_for('users.profile'))
    return render_template('users/update_password.html', form=form)


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
            form.logo = os.path.join('static/img/', filename)
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

    if role == 'sponsor':
            sponsor = Sponsor.query.filter_by(company_name=form.company.data).first()
            if sponsor:
                flash('Email address already exists.')
                return render_template('users/register.html', form=form)
            new_sponsor = Sponsor(form.company.data, form.logo, form.email.data, form.phone.data, form.company_website.data, new_user.get_id())
            db.session.add(new_sponsor)
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