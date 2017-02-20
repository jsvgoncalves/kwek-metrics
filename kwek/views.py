# -*- coding: utf-8 -*-
#
# This file is part of Kwek Metrics.
""" Kwek Views. """

from flask import request, render_template, flash, Blueprint
from model import Service, Metric
from urlparse import urljoin
from database import db
import json

# For the Form
from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, BooleanField, SelectField
from wtforms.validators import DataRequired, Regexp
from wtforms_alchemy import ModelForm

from api.hawkular import get_os_projects
from api.hawkular import get_metric


blueprint = Blueprint('kwek', __name__,
                      template_folder='templates')


class ServiceForm(ModelForm, Form):
    """Handle subscribe form neatly with WTForms."""
    class Meta:
        model = Service

    name = StringField(u'Name:', validators=[DataRequired()])
    token = StringField(u'Service', validators=[DataRequired()])


class MetricForm(ModelForm, Form):
    """Handle subscribe form neatly with WTForms."""
    class Meta:
        model = Metric

    name = StringField(u'Name:', validators=[DataRequired()])
    api_name = StringField(u'Service', validators=[DataRequired()])


@blueprint.route('/', methods=['GET', 'POST'])
def index():
    """Returns the newly added services since the last request.

    API used by the backend application
    """
    services = []
    for row in Service.query.all():
        services.append(row)
    return render_template('list.html', services=json.dumps(services))


@blueprint.route('/insert', methods=['GET'])
def insert():
    services = []
    for row in Service.query.all():
        services.append(row)
    return render_template(
        'insert_service.html',
        services=services)


@blueprint.route('/stats', methods=['GET'])
def stats():
    s = Service.query.filter_by().first()
    try:
        projects = get_os_projects(
            'https://console.engint.openshift.com/oapi/v1/projects',
            s.token)
    except ValueError as err:
        projects = {}
        flash(err.args)

    # Get Metrics for each of the projects
    total_memory = 0
    total_cpu = 0
    total_network = 0
    for project in projects:
        try:
            memory = get_metric(
                urljoin(s.url, 'gauges/data'),
                project['metadata']['name'],
                s.token,
                'memory%2Fusage')
            total_memory += memory[0]['avg']
        except ValueError as err:
            flash(project['metadata']['name'], err.message)
        except KeyError as err:
            flash(project['metadata']['name'], err.message)

    return render_template(
        'stats.html',
        projects=projects,
        memory=total_memory,
        cpu=total_cpu,
        network=total_network)


@blueprint.route('/metrics/<project>', methods=['GET'])
def metrics(project):
    s = Service.query.filter_by().first()
    try:
        memory = get_metric(
            urljoin(s.url, 'gauges/data'),
            project,
            s.token,
            'memory%2Fusage')

        cpu = get_metric(
            urljoin(s.url, 'gauges/data'),
            project,
            s.token,
            'cpu%2Fusage_rate')

        network = get_metric(
            urljoin(s.url, 'gauges/data'),
            project,
            s.token,
            'network%2Frx_rate')
    except ValueError as err:
        flash(err.args)
    return render_template('metrics.html',
                           project=project,
                           memory=memory,
                           cpu=cpu,
                           network=network)


@blueprint.route('/insert', methods=['POST'])
def form_subscribe(data):
    """Handle subscription form submission."""
    try:
        # Try to find an existing user to update
        u = Service.query.filter_by(name=e_data['name']).first()
        # !TODO: This requires refactoring..
        if u:
            # Update Service
            u.name = e_data['name']
            u.token = e_data['token']
        else:
            # Create new Service
            u = Service(e_data['name'],
                     e_data['token'])
        db.session.add(u)
        db.session.commit()
        return True
    except Exception, e:
        print('form_subscribe():', str(e))
        flash(u'Saving to database failed.', 'Error')
        # Should return the errors (possibly duplicate or?)
        return False
