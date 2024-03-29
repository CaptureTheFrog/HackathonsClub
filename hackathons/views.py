from flask import Blueprint, render_template, redirect, url_for
from db import db
from models.hackathon import Hackathon
from users.forms import CreateEventForm
from utils.decorators import requires_roles
from flask_login import login_required

hackathons_blueprint = Blueprint('hackathons', __name__, template_folder='templates', static_folder='static', url_prefix='/hackathons')


@hackathons_blueprint.route('')
def hackathons():
    return render_template('hackathons/hackathons.html', data=db.session.query(Hackathon).all())


@hackathons_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
@requires_roles('organizer')
def create():
    form = CreateEventForm()
    if form.validate_on_submit():
        db.session.add(Hackathon(form.title.data, form.start_date.data, form.end_date.data, form.location.data, 'Hackathon', '', '', '', '', form.website.data))
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('hackathons/create.html', form=form)


@hackathons_blueprint.route('/sponsor_events', methods=['GET', 'POST'])
@login_required
@requires_roles('sponsor')
def sponsor_events():
    return render_template('hackathons/sponsor_events.html')
    # Placeholder code
    # events = Event.query.all() # change table name
    # return render_template('events/sponsor_events.html', events=events)


@hackathons_blueprint.route('/postings', methods=['GET', 'POST'])
@login_required
@requires_roles('organizer')
def postings():
    return render_template('hackathons/postings.html')
    # Placeholder code
    # postings = Posting.query.all() # change table name
    # return render_template('events/postings.html', postings=postings)


@hackathons_blueprint.route('/sponsors', methods=['GET', 'POST'])
@login_required
@requires_roles('organizer')
def sponsors():
    return render_template('hackathons/sponsors.html')
    # Placeholder code
    # show all sponsors