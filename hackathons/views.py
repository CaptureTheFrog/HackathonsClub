from flask import Blueprint, render_template
from db import db
from models.hackathon import Hackathon
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
    return render_template('hackathons/create.html')
    # Placeholder code
    # form = EventForm()
    # if form.validate_on_submit():
    #     event = Event.query.filter_by(name=form.name.data).first() # change table name
    #     if event:
    #         flash('Event already exists')
    #         return render_template('events/create.html', form=form)
    #     new_event = Event(name=form.name.data,
    #                         description=form.description.data,
    #                         date=form.date.data,
    #                         location=form.location.data,
    #                         capacity=form.capacity.data)
    #     db.session.add(new_event)
    #     db.session.commit()
    #     flash('Event created')
    #     return redirect(url_for('events.index'))
    # return render_template('events/create.html', form=form)


@hackathons_blueprint.route('/sponsor_events', methods=['GET', 'POST'])
@login_required
@requires_roles('sponsor')
def sponsor_events():
    return render_template('hackathons/sponsor_events.html')
    # Placeholder code
    # events = Event.query.all() # change table name
    # return render_template('events/sponsor_events.html', events=events)
