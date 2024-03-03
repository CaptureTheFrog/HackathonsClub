from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from users.forms import LoginForm, UserRegistrationForm, SponsorRegistrationForm
from models.user import User
from app import db

users_blueprint = Blueprint('users', __name__, template_folder='templates')


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
        return redirect(url_for('main.index'))
    return render_template('users/login.html', form=form)


@users_blueprint.route('/logout')
@login_required
# @requires_roles('user', 'admin') TODO: CHANGE
def logout():
    # log out user
    logout_user()
    # redirect user to index page
    return redirect(url_for('main.index')) # TODO: or just index?


def register_user(form, role):
    user = User.query.filter_by(email=form.email.data).first()
    if user:
        flash('Email address already exists.')
        return render_template('users/register.html', form=form)
    new_user = User(email=form.email.data,
                    password=form.password.data,
                    role=role)
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)
    return redirect(url_for('main.index'))


@users_blueprint.route('/register/participant', methods=['GET', 'POST'])
def participant_registration():
    form = UserRegistrationForm()
    if form.validate_on_submit():
        register_user(form, 'participant')
        return redirect(url_for('main.index'))
    return render_template('users/register.html', form=form, role='participant')


@users_blueprint.route('/register/organizer', methods=['GET', 'POST'])
def organizer_registration():
    form = UserRegistrationForm()
    if form.validate_on_submit():
        register_user(form, 'organizer')
        return redirect(url_for('main.index'))
    return render_template('users/register.html', form=form, role='organizer')


@users_blueprint.route('/register/sponsor', methods=['GET', 'POST'])
def sponsor_registration():
    form = SponsorRegistrationForm()
    if form.validate_on_submit():
        register_user(form, 'sponsor')
        return redirect(url_for('main.index'))
    return render_template('users/register.html', form=form, role='sponsor')


@users_blueprint.route('/role_selection')
def role_selection():
    return render_template('users/role_selection.html')