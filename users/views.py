from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from users.forms import LoginForm
from models.user import User
import bcrypt

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


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('users/register.html')