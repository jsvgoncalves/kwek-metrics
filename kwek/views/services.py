# -*- coding: utf-8 -*-
#
# This file is part of Kwek Metrics.

"""Kwek Metrics Service CRUD views."""

from flask import render_template, flash, Blueprint, request, redirect,\
    url_for, abort
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms_alchemy import ModelForm

from kwek.models import Service
from kwek.database import db

blueprint = Blueprint('services', __name__,
                      template_folder='../templates/services/',
                      url_prefix='/services')


class ServiceForm(ModelForm, Form):
    """Handle subscribe form neatly with WTForms."""
    class Meta:
        csrf = False
        model = Service

    name = StringField(u'Name', validators=[DataRequired()])
    token = StringField(u'Token', validators=[DataRequired()])
    hwk_url = StringField(u'Hawkular URL', validators=[DataRequired()])
    os_url = StringField(u'OpenShift URL', validators=[DataRequired()])


@blueprint.route('/<id>', methods=['GET'])
def get(id):
    """Return a Service."""
    result = Service.query.get(id)
    if result:
        form = ServiceForm(obj=result)
        service = result.serialized
    else:
        abort(404)
    return render_template(
        'services/service.html',
        service=service,
        form=form)


@blueprint.route('/', methods=['GET'])
def index():
    """Return a list of Services."""
    form = ServiceForm()
    services = [service.serialized for service in Service.query.all()]
    return render_template(
        'services/index.html',
        services=services,
        form=form)


@blueprint.route('/delete/<id>', methods=['POST'])
def delete(id):
    """Delete a Service."""
    service = Service.query.get(id)
    if service:
        try:
            db.session.delete(service)
            db.session.commit()
            flash('Service {0} deleted.'.format(service.name), 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error: {0}'.format(e.message), 'danger')
        finally:
            return redirect(url_for('.index'))
    else:
        abort(404)


@blueprint.route('/insert', methods=['POST'])
def insert():
    """Create a new Service.

    Redirect to services/ page if succesfull,
    Return the services template with the errors otherwise
    """
    form = ServiceForm(request.form)
    if form.validate():
        try:
            service = Service(form.name.data, form.token.data,
                              form.hwk_url.data, form.os_url.data)
            db.session.add(service)
            db.session.commit()
            flash('Service {0} created.'.format(form.name.data), 'success')
            return redirect(url_for('.index'))
        except Exception as e:
            db.session.rollback()
            flash('Error: {0}'.format(e.message), 'danger')

    # If the validation or insertion failed, present the errors w/ template
    return render_template('services/insert.html',
                           form=form)


@blueprint.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    """Update a Service.

    redirect to services/ page if succesfull,
    return the services template with the errors otherwise
    """
    service = Service.query.get(id)
    if not service:
        abort(404)

    if request.method == 'GET':
        form = ServiceForm(obj=service)
        return render_template(
            'services/update.html',
            service=service.serialized,
            form=form)

    elif request.method == 'POST':
        form = ServiceForm(request.form)
        if form.validate():
            try:
                # Set the new fields
                # !TODO: is there a better way to do this?
                #        check form.data for a dict
                service.name = form.name.data
                service.token = form.token.data
                service.hwk_url = form.hwk_url.data
                service.os_url = form.os_url.data

                # Do the update
                db.session.add(service)
                db.session.commit()
                flash('Service {0} updated.'.format(form.name.data), 'success')
                return redirect(url_for('.index'))
            except Exception as e:
                db.session.rollback()
                flash('Error: {0}'.format(e.message), 'danger')

        # If the validation or insertion failed, present the errors w/ template
        return render_template('services/update.html',
                               service=service,
                               form=form)
