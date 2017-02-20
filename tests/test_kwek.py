# -*- coding: utf-8 -*-
#
# This file is part of Kwek Metrics.

"""Module tests."""
from __future__ import absolute_import, print_function

from flask import Flask


def test_view(app):
    """Test view."""
    print(type(app))
    with app.test_client() as client:
        res = client.get("/")
        assert res.status_code == 404
        # assert 'Welcome to kwek' in str(res.data)
