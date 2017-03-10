# -*- coding: utf-8 -*-
#
# This file is part of Kwek Metrics.

"""Kwek Metric web app views."""

from urlparse import urljoin

from flask import render_template, flash, Blueprint, redirect, url_for

from api.hawkular import get_os_projects
from api.hawkular import get_metric
from kwek.models import Service, Metric


blueprint = Blueprint('kwek', __name__,
                      template_folder='../templates')


@blueprint.route('/', methods=['GET'])
def index():
    """Home page.
    Return a list of all the projects and it's top-level metrics.
    """
    s = Service.query.filter_by().first()
    if s is None:
        flash('No Service found. Please add one below.', 'danger')
        return redirect(url_for('services.index'))
    try:
        projects = get_os_projects(
            urljoin(s.os_url, 'projects'),
            s.token)
    except (ValueError, AttributeError) as err:
        projects = {}
        flash(err.args)
    metrics = Metric.query.all()

    # Get the values for each metric, per project
    values = {}
    for project in projects:
        values[project['metadata']['name']] = {}
        try:
            for metric in metrics:
                v = get_metric(
                    urljoin(s.hwk_url, metric.endpoint),
                    project['metadata']['name'],
                    s.token,
                    metric.tag)
                values[project['metadata']['name']][metric.name] = v
        except ValueError as err:
            flash(project['metadata']['name'], err.message)
        except KeyError as err:
            flash(project['metadata']['name'], err.message)

    # Calculate the aggregated value of each metric
    totals = {}
    for metric in metrics:
        totals[metric.name] = 0
        for project in projects:
            try:
                # Get the last measure for the given metric
                last_measure = values[
                    project['metadata']['name']][metric.name][0]
                # And sum it to our total per metric
                totals[metric.name] += last_measure['avg']
            except KeyError as err:
                flash('Error retrieving metric [KeyError]', 'danger')

    return render_template(
        'index.html',
        projects=projects,
        metrics=metrics,
        values=values,
        totals=totals)


@blueprint.route('/stats/<project>', methods=['GET'])
def stats(project):
    s = Service.query.filter_by().first()
    metrics = Metric.query.all()
    values = {}
    try:
        for metric in metrics:
            values[metric.name] = get_metric(
                urljoin(s.hwk_url, metric.endpoint),
                project,
                s.token,
                metric.tag)
    except ValueError as err:
        flash(err.args)
    return render_template('stats.html',
                           project=project,
                           metrics=metrics,
                           values=values)
