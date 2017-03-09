# -*- coding: utf-8 -*-
#
# This file is part of Kwek Metrics.

"""Kwek Metrics Metric CRUD views."""

from flask import render_template, flash, Blueprint, request, redirect,\
    url_for, abort
from flask_wtf import Form
from wtforms import StringField, FloatField
from wtforms.validators import InputRequired
from wtforms_alchemy import ModelForm

from kwek.models import Metric
from kwek.database import db

blueprint = Blueprint('metrics', __name__,
                      template_folder='../templates/metrics/',
                      url_prefix='/metrics')


class MetricForm(ModelForm, Form):
    """Handle subscribe form neatly with WTForms."""
    class Meta:
        model = Metric

    name = StringField(u'Name:', validators=[InputRequired()])
    display_name = StringField(u'display_name:', validators=[InputRequired()])
    endpoint = StringField(u'endpoint:', validators=[InputRequired()])
    tag = StringField(u'tag:', validators=[InputRequired()])
    unit = StringField(u'unit:', validators=[InputRequired()])
    conversion = FloatField(u'conversion:', validators=[InputRequired()])
    color = StringField(u'color:', validators=[InputRequired()])


def get(id):
    """Return a Metric."""
    result = Metric.query.get(id)
    if result:
        form = MetricForm(obj=result)
        metric = result.serialized
    else:
        abort(404)
    return render_template(
        'metrics/metric.html',
        metric=metric,
        form=form)


@blueprint.route('/', methods=['GET'])
def index():
    """Return a list of Metrics."""
    form = MetricForm()
    metrics = [metric.serialized for metric in Metric.query.all()]
    return render_template(
        'metrics/index.html',
        metrics=metrics,
        form=form)


@blueprint.route('/delete/<id>', methods=['POST'])
def delete(id):
    """Delete a Metric."""
    metric = Metric.query.get(id)
    if metric:
        try:
            db.session.delete(metric)
            db.session.commit()
            flash('Metric {0} deleted.'.format(metric.name), 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error: {0}'.format(e.message), 'danger')
        finally:
            return redirect(url_for('.index'))
    else:
        abort(404)


@blueprint.route('/insert', methods=['POST'])
def insert():
    """Create a new Metric.

    Redirect to metrics/ page if succesfull,
    Return the metrics template with the errors otherwise
    """
    form = MetricForm(request.form)
    if form.validate():
        try:
            metric = Metric(
                form.name.data,
                form.display_name.data,
                form.endpoint.data,
                form.tag.data,
                form.unit.data,
                form.conversion.data,
                form.color.data)
            db.session.add(metric)
            db.session.commit()
            flash('Metric {0} created.'.format(form.name.data), 'success')
            return redirect(url_for('.index'))
        except Exception as e:
            db.session.rollback()
            flash('Error: {0}'.format(e.message), 'danger')

    # If the validation or insertion failed, present the errors w/ template
    return render_template('metrics/insert.html',
                           form=form)


@blueprint.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    """Update a Metric.

    redirect to metrics/ page if succesfull,
    return the metrics template with the errors otherwise
    """
    metric = Metric.query.get(id)
    if not metric:
        abort(404)

    if request.method == 'GET':
        form = MetricForm(obj=metric)
        return render_template(
            'metrics/update.html',
            metric=metric.serialized,
            form=form)

    elif request.method == 'POST':
        form = MetricForm(request.form)
        if form.validate():
            try:
                # Set the new fields
                # !TODO: is there a better way to do this?
                #        check form.data for a dict
                metric.name = form.name.data
                metric.display_name = form.display_name.data
                metric.endpoint = form.endpoint.data
                metric.tag = form.tag.data
                metric.unit = form.unit.data
                metric.conversion = form.conversion.data
                metric.color = form.color.data

                # Do the update
                db.session.add(metric)
                db.session.commit()
                flash('Metric {0} updated.'.format(form.name.data), 'success')
                return redirect(url_for('.index'))
            except Exception as e:
                db.session.rollback()
                flash('Error: {0}'.format(e.message), 'danger')

        # If the validation or insertion failed, present the errors w/ template
        return render_template('metrics/update.html',
                               metric=metric,
                               form=form)
