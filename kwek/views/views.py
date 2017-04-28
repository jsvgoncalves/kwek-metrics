# -*- coding: utf-8 -*-
#
# This file is part of Kwek Metrics.

"""Kwek Metric web app views."""

from urlparse import urljoin

from flask import render_template, flash, Blueprint, redirect, url_for
from requests import ConnectionError

from api.hawkular import get_os_projects
from api.hawkular import get_metric
from api.hawkular import get_metrics
from api.hawkular import APIAuthorizationError
from kwek.models import Service, Metric
from kwek.database import db

blueprint = Blueprint('kwek', __name__,
                      template_folder='../templates')


@blueprint.route('/', methods=['GET'])
def index():
    s = Service.query.filter_by().first()
    if s is None:
        flash('No Service found. Please add one below.', 'danger')
        return redirect(url_for('services.index'))
    try:
        projects = get_os_projects(
            urljoin(s.os_url, 'projects'),
            s.token)
    except (ValueError, AttributeError, ConnectionError) as err:
        projects = {}
        flash(err.message, 'danger')
    except APIAuthorizationError as err:
        flash(err.message, 'danger')
        return redirect(url_for('services.index'))
    # Build the query string
    # https://metrics.engint.openshift.com/hawkular/metrics/metrics/stats/query
    # {"tags":"descriptor_name:network/tx_rate|network/rx_rate,type:pod","buckets":"1"}
    # {"tags":"descriptor_name:memory/usage|cpu/usage_rate,type:pod_container","buckets":"1"}
    metrics_pod = {
        'endpoint': 'metrics/stats/query',
        'type': 'pod_container',
        'queries': [
            {'conversion': 9.53674e-07,
             'display_name': 'Memory Usage',
             'name': 'memory', 'color': 'blue', 'tag': 'memory/usage',
             'id': 2, 'unit': 'MiB', 'maxvalue': 836868241},
            {'conversion': 1.0,
             'display_name': 'CPU Usage',
             'name': 'cpu', 'color': 'red', 'tag': 'cpu/usage_rate',
             'id': 2, 'unit': 'Millicores', 'maxvalue': 0}
        ]
    }

    # Initialize the metric totals
    totals = {}
    # And the tags for the API request
    tags = []
    for metric in metrics_pod['queries']:
        tags.append(metric['tag'])
        totals[metric['tag']] = 0

    # Initialize metric values dict
    values = {}
    for p in projects:
        # Initialize metric for the project
        name = p['metadata']['name']
        values[name] = {'avg': {}}
        for tag in tags:
            # Initialize metric tags for the project
            values[name]['avg'][tag] = 0
            values[name][tag] = []
        try:
            # Get all the metrics for the project
            v = get_metrics(
                urljoin(s.hwk_url, metrics_pod['endpoint']),
                name,
                s.token,
                tags,
                'pod_container')  # !TODO: Replace with dynamic value
            # Iterate over the values
            for k, v in v['gauge'].iteritems():
                # Filter out `sti-build` values, e.g.:
                # "sti-build/7c197071-193a-11e7-8dbe-126ee6b1d97f/cpu/usage_rate"
                if k.partition('/')[0] != 'sti-build':
                    # Filter out Empty values
                    if v[0]['empty'] is False:
                        # Append each metric to its proper tag
                        for tag in tags:
                            if tag in k:
                                values[name][tag].append(v)
                                values[name][
                                    'avg'][tag] += v[0]['avg']
                                totals[tag] += v[0]['avg']
        except Exception as err:
            flash('{} - {}'.format(name, err.message), 'danger')

    for k, v in values.iteritems():
        pass

    return render_template(
        'index.html',
        projects=projects,
        values=values,
        metrics=metrics_pod['queries'],
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
    except (ValueError, ConnectionError) as err:
        flash(err.message, 'danger')
    return render_template('stats.html',
                           project=project,
                           metrics=metrics,
                           values=values)


default_service = {
    'name': 'OpenShift Dedicated',
    'token': 'this_will_be_updated',
    'hawkular': 'https://metrics.engint.openshift.com/hawkular/metrics/',
    'openshift': 'https://console.engint.openshift.com/oapi/v1/'
}


default_metrics = {
    'endpoint': 'metrics/stats/query',
    'type': 'pod_container',
    'queries': [
        {'conversion': 9.53674e-07,
         'display_name': 'Memory Usage',
         'name': 'memory', 'color': 'blue', 'tag': 'memory/usage',
         'id': 2, 'unit': 'MiB', 'max': 64424509440},
        {'conversion': 1.0,
         'display_name': 'CPU Usage',
         'name': 'cpu', 'color': 'red', 'tag': 'cpu/usage_rate',
         'id': 2, 'unit': 'Millicores', 'max': 16000}
    ]
}


@blueprint.route('/defaults')
def defaults():
    try:
        s = default_service
        service = Service(s['name'], s['token'],
                          s['hawkular'], s['openshift'])
        db.session.add(service)
        m0 = default_metrics['queries'][0]
        m1 = default_metrics['queries'][1]
        memory_metric = Metric(
            m0['name'],
            m0['display_name'],
            default_metrics['endpoint'],
            m0['tag'],
            m0['unit'],
            m0['conversion'],
            m0['max'],
            m0['color'])

        cpu_metric = Metric(
            m1['name'],
            m1['display_name'],
            default_metrics['endpoint'],
            m1['tag'],
            m1['unit'],
            m1['conversion'],
            m1['max'],
            m1['color'])

        db.session.add(memory_metric)
        db.session.add(cpu_metric)
        db.session.commit()
        flash('Service `{}` created. Please update the token.'.format(
            s['name']), 'success')
        flash('Metric `{}` created.'.format(m0['name']), 'success')
        flash('Metric `{}` created.'.format(m1['name']), 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error: {0}'.format(e.message), 'danger')
    return redirect(url_for('services.index'))
