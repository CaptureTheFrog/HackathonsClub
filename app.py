from flask import Flask, render_template
from flask_login import LoginManager, current_user

from models.hackathon import Hackathon
from utils.import_hackathons_to_db import import_hackathons_to_db

app = Flask(__name__)

db_name = 'hacksclub.db'
app.config['SECRET_KEY'] = 'ABigFatSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from db import db

db.init_app(app)

from models.user import User
from models.sponsor import Sponsor
from models.hackathon import Hackathon

# Create or upgrade the database within the application context
with app.app_context():
    db.create_all()
    # uncomment to add hackathons to db
    if len(db.session.query(Hackathon).all()) == 0:
        import_hackathons_to_db(db)

from users.views import users_blueprint
from hackathons.views import hackathons_blueprint

app.register_blueprint(users_blueprint)
app.register_blueprint(hackathons_blueprint)

from functools import wraps


def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.role not in roles:
                return render_template('errors/403.html')
            return f(*args, **kwargs)
        return wrapped
    return wrapper


login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
def index():
    return render_template('main/index.html')

@app.errorhandler(400)
def bad_request(error):
    return render_template("errors/400.html"), 400


@app.errorhandler(403)
def access_denied(error):
    return render_template("errors/403.html"), 403


@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template("errors/500.html"), 500


@app.errorhandler(503)
def service_unavailable(error):
    return render_template("errors/503.html"), 503


if __name__ == '__main__':
    app.run()