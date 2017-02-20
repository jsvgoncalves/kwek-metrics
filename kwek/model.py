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
    url = db.Column(db.String(120), unique=True)

    def __init__(self, name, token, url):
        self.name = name
        self.token = token
        self.url = url

    def __repr__(self):
        return '<Service %r : %r (%r)>' % (self.name, self.url, self.token)


class Metric(db.Model):
    """Database model for SQLAlchemy."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    api_name = db.Column(db.String(120), unique=True)

    def __init__(self, name, api_name):
        self.name = name
        self.api_name = api_name

    def __repr__(self):
        return '<Metric %r : %r>' % (self.name, self.api_name)
