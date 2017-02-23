# -*- coding: utf-8 -*-
#
# This file is part of Kwek Metrics.

"""Database models for Services and Metrics."""

from database import db


class Service(db.Model):
    """Database model for SQLAlchemy."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    token = db.Column(db.String(120), unique=True)
    hwk_url = db.Column(db.String(120), unique=True)
    os_url = db.Column(db.String(120), unique=True)

    def __init__(self, name, token, hwk_url, os_url):
        self.name = name
        self.token = token
        self.hwk_url = hwk_url
        self.os_url = os_url

    def __repr__(self):
        return '<Service %r : %r>' % (self.name, self.os_url)


class Metric(db.Model):
    """Database model for SQLAlchemy."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    display_name = db.Column(db.String(120))
    endpoint = db.Column(db.String(80))
    tag = db.Column(db.String(80), unique=True)
    unit = db.Column(db.String(80))
    conversion = db.Column(db.Float)

    def __init__(self, name, display_name, endpoint, tag, unit, conversion):
        self.name = name
        self.display_name = display_name
        self.endpoint = endpoint
        self.tag = tag
        self.unit = unit
        self.conversion = conversion

    def __repr__(self):
        return '<Metric %r : %r>' % (self.name, self.display_name)
