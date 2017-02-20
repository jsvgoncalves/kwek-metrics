# -*- coding: utf-8 -*-
#
# This file is part of Kwek Metrics.

from kwek.model import Service as S
from kwek.model import Metric as M


def test_service_insert(session):
    """Test the User insertion."""
    assert S.query.count() == 0
    s = S('name',
          'url',
          'token')
    session.add(s)
    assert S.query.count() == 1


def test_metric_insert(session):
    """Test the User insertion."""
    assert M.query.count() == 0
    m = M('name',
          'email')
    session.add(m)
    assert M.query.count() == 1


def test_routes(client, session):
    """Test the available routes and their accessible methods."""
    pass
    # index should allow both GET and POST requests
    # assert client.get(
    #     url_for('kwek.get_subscribers')).status_code == 200
    # assert client.post(
    #     url_for('kwek.get_subscribers')).status_code == 200
