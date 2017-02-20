# -*- coding: utf-8 -*-
#
# This file is part of Kwek Metrics.

"""Kwek database configurations."""

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker

db = SQLAlchemy()
session = scoped_session(sessionmaker())
