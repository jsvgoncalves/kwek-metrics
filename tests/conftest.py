# -*- coding: utf-8 -*-
#
# This file is part of Kwek Metrics.

"""Pytest configuration."""

from __future__ import absolute_import, print_function

import pytest
from flask import Flask


@pytest.fixture()
def app():
    """Flask application fixture."""
    app = Flask('testapp')
    app.config.update(
        TESTING=True
    )
    return app
