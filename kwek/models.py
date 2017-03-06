# -*- coding: utf-8 -*-
#
# This file is part of Kwek Metrics.

"""Database models for Services and Metrics."""

from database import db


def to_dict(inst, cls):
    """Return a dict with the sql alchemy table columns."""
    convert = dict()
    # add your coversions for things like datetime's
    # and what-not that aren't serializable.
    d = dict()
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        if c.type in convert.keys() and v is not None:
            try:
                d[c.name] = convert[c.type](v)
            except:
                d[c.name] = "Error:  Failed to covert using ", str(convert[
                                                                   c.type])
        elif v is None:
            d[c.name] = str()
        else:
            d[c.name] = v
    return d


class Serializable(object):
    """Mixin to make objects serializable."""
    @property
    def serialized(self):
        """Return object data in easily serializeable format"""
        return to_dict(self, self.__class__)


class Service(db.Model, Serializable):
    """Database model for SQLAlchemy."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    token = db.Column(db.String(120))
    hwk_url = db.Column(db.String(120))
    os_url = db.Column(db.String(120))

    def __init__(self, name, token, hwk_url, os_url):
        self.name = name
        self.token = token
        self.hwk_url = hwk_url
        self.os_url = os_url

    def __repr__(self):
        return '<Service %r : %r>' % (self.name, self.os_url)


class Metric(db.Model, Serializable):
    """Database model for SQLAlchemy."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    display_name = db.Column(db.String(120))
    endpoint = db.Column(db.String(80))
    tag = db.Column(db.String(80), unique=True)
    unit = db.Column(db.String(80))
    conversion = db.Column(db.Float)
    color = db.Column(db.String(80))

    def __init__(self, name, display_name, endpoint,
                 tag, unit, conversion, color):
        self.name = name
        self.display_name = display_name
        self.endpoint = endpoint
        self.tag = tag
        self.unit = unit
        self.conversion = conversion
        self.color = color

    def __repr__(self):
        return '<Metric %r : %r>' % (self.name, self.display_name)
