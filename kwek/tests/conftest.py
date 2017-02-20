# -*- coding: utf-8 -*-
#
# This file is part of Kwek Metrics.

"""Pytest configuration."""

from os.path import join as pj
import os.path

import pytest

from app import create_app
from kwek.database import db as _db


@pytest.yield_fixture(scope='function')
def app(request):
    """Create the Flask app."""
    app = create_app()
    app.config['TESTING'] = True
    # CSRF checks should be disabled or inserting a user
    # via the appropriate view will fail
    app.config.update(dict(WTF_CSRF_ENABLED=False))
    yield app


@pytest.yield_fixture(scope='function')
def db(app, request):
    """Initialize the test database.

    Function scoped is required for the fixture, as the views logic
    does session.commit() calls, which can't be rolled back and would
    polute the remaining tests.
    """
    # Updates the database file to a temporary one
    TESTDB_PATH = pj(app.root_path, 'tmp.db')
    TEST_DATABASE_URI = 'sqlite:///' + TESTDB_PATH
    app.config.update(dict(TESTDB_PATH=TESTDB_PATH))
    app.config.update(dict(SQLALCHEMY_DATABASE_URI=TEST_DATABASE_URI))

    # Check if the file already exists and if so, delete it
    if os.path.exists(app.config['TESTDB_PATH']):
        os.unlink(app.config['TESTDB_PATH'])

    # Init db and make it accessible to the app
    _db.init_app(app)
    with app.app_context():
        _db.create_all()

    # Yield the db
    yield _db

    # Teardown code
    # Drop tables and delete the database file
    with app.app_context():
        _db.drop_all()
    os.unlink(app.config['TESTDB_PATH'])


@pytest.yield_fixture(scope='function')
def session(db, request):
    """Create a new session with app and db access for a test function."""

    _session = db.session
    yield _session

    # Teardown code
    # The session needs to be rolled back or the db.drop_all()
    # will fail due to pending changes
    _session.rollback()
