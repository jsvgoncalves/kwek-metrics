# -*- coding: utf-8 -*-
#
# This file is part of Kwek Metrics.

"""Kwek Metric web app views."""

from urlparse import urljoin

from flask import render_template, flash, Blueprint
from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms_alchemy import ModelForm

from api.hawkular import get_os_projects
from api.hawkular import get_metric
from database import db
from model import Service, Metric


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


@blueprint.route('/', methods=['GET'])
def index():
    """Home page.
    Return a list of all the projects and it's top-level metrics.
    """
    s = Service.query.filter_by().first()
    try:
        projects = get_os_projects(
            urljoin(s.os_url, 'projects'),
            s.token)
    except ValueError as err:
        projects = {}
        flash(err.args)

    # Metrics to query for
    # !TODO: Extract to database
    metrics = {
        'memory': {
            'name': 'Memory Usage',
            'endpoint': 'gauges/data',
            'tag': 'memory%2Fusage',
            'unit': 'MiB',
            'conversion': 0.000000953674
        },
        'cpu': {
            'name': 'CPU Usage',
            'endpoint': 'gauges/data',
            'tag': 'cpu%2Fusage_rate',
            'unit': 'Millicores',
            'conversion': 1
        },
        'network': {
            'name': 'Network Usage',
            'endpoint': 'gauges/data',
            'tag': 'network%2Frx_rate',
            'unit': 'KiB/s',
            'conversion': 0.0009765625
        }
    }

    # Get the values for each metric, per project
    values = {}
    for project in projects:
        values[project['metadata']['name']] = {}
        try:
            for metric, cfg in metrics.iteritems():
                v = get_metric(
                    urljoin(s.hwk_url, cfg['endpoint']),
                    project['metadata']['name'],
                    s.token,
                    cfg['tag'])
                values[project['metadata']['name']][metric] = v
        except ValueError as err:
            flash(project['metadata']['name'], err.message)
        except KeyError as err:
            flash(project['metadata']['name'], err.message)

    # Calculate the aggregated value of each metric
    totals = {}
    for metric in metrics:
        totals[metric] = 0
        for project in projects:
            # Get the last measure for the given metric
            last_measure = values[project['metadata']['name']][metric][0]
            # And sum it to our total per metric
            totals[metric] += last_measure['avg']

    return render_template(
        'stats.html',
        projects=projects,
        metrics=metrics,
        values=values,
        totals=totals)


@blueprint.route('/insert', methods=['GET'])
def insert():
    services = []
    for row in Service.query.all():
        services.append(row)
    return render_template(
        'insert_service.html',
        services=services)


@blueprint.route('/metrics/<project>', methods=['GET'])
def metrics(project):
    s = Service.query.filter_by().first()
    try:
        # !TODO: Adopt same logic as index():
        memory = get_metric(
            urljoin(s.hwk_url, 'gauges/data'),
            project,
            s.token,
            'memory%2Fusage')

        cpu = get_metric(
            urljoin(s.hwk_url, 'gauges/data'),
            project,
            s.token,
            'cpu%2Fusage_rate')

        network = get_metric(
            urljoin(s.hwk_url, 'gauges/data'),
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
