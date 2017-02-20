#!/usr/bin/env python

# -*- coding: utf-8 -*-
#
# This file is part of Kwek Metrics.
# This file may be used instead of Apache mod_wsgi to run your python
# web application in a different framework.  A few examples are
# provided (cherrypi, gevent), but this file may be altered to run
# whatever framework is desired - or a completely customized service.
#
from __future__ import print_function
from importlib import import_module

from flask import Flask

from kwek.database import db


def register_blueprints(app, blueprints):
    """Registers the blueprints given by loading their module

    Note: If a module fails to load the blueprint will be ignored.

    :param app: flask application object
    :param blueprints: list of module names with blueprints
    """
    try:
        for b in blueprints:
            # All blueprints should have a views.py file with the blueprint
            mod = import_module(b + '.views')
            app.register_blueprint(mod.blueprint)
    except Exception, e:
        print('register_blueprint(): ', str(e))


def create_app(cfg_file='app.cfg'):
    """Creates the flask app and inits the db

    :returns: flask application object"""
    # Init flask app and load configs
    app = Flask(__name__)
    # app.config.from_pyfile(cfg_file)
    app.config.from_pyfile(cfg_file)

    # Register all the blueprints
    blueprints = ['kwek']
    register_blueprints(app, blueprints)

    return app

if __name__ == '__main__':
    app = create_app()
    from os.path import join as pj
    app.config.update(dict(
        SQLALCHEMY_DATABASE_URI='sqlite:///' +
                                pj(app.root_path, 'kwek.db')
    ))

    # Init db and make it accessible to the app
    db.init_app(app)
    with app.app_context():
        db.create_all()

    port = app.config['PORT']
    ip = app.config['IP']
    app_name = app.config['APP_NAME']
    host_name = app.config['HOST_NAME']

    server = Flask(__name__)
    server.wsgi_app = app
    server.run(host=ip, port=port, use_reloader=True)
