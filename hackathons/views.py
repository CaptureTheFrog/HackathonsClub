from flask import Blueprint, render_template
from db import db
from models.hackathon import Hackathon

hackathons_blueprint = Blueprint('hackathons', __name__, template_folder='templates', static_folder='static', url_prefix='/hackathons')


@hackathons_blueprint.route('')
def hackathons():
    return render_template('hackathons/hackathons.html', data=db.session.query(Hackathon).all())
