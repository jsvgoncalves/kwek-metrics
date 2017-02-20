# -*- coding: utf-8 -*-
#
# This file is part of Kwek Metrics.

"""Pytest configuration."""

from os import path as osp
import json

import pytest

mock_api_query_body = """
    [
    {
        u'end': 1487239169330,
        u'min': 1104474112.0,
        u'max': 1207738368.0,
        u'sum': 4624379904.0,
        u'median': 1206710272.0,
        u'start': 1487239109330,
        u'samples': 6,
        u'avg': 1181607936.0,
        u'empty': False
    },
    {
        u'end': 1487239229330,
        u'min': 1207025664.0,
        u'max': 1208631296.0,
        u'sum': 4831559680.0,
        u'median': 1207853056.0,
        u'start': 1487239169330,
        u'samples': 6,
        u'avg': 1207889920.0,
        u'empty': False}
    ]
    """


@pytest.fixture(scope='function')
def mock_hawkular_api():
    def f(r):
        if 'Hawkular-Tenant' not in r.headers:
            return (400, "", "Bad Request")
        if 'Accept' not in r.headers:
            return (400, "", "Bad Request")
        if 'Authorization' not in r.headers:
            return (400, "", "Bad Request")
        path = osp.join(osp.dirname(osp.realpath(__file__)),
                        'mock_api_json_replies',
                        'hawkular_cpu_metric.json')
        with open(path) as data_file:
            data = json.load(data_file)
        headers = {'r-id': '728d329e-0e86-11e4-a748-0c84dc037c13'}
        return (200, headers, json.dumps(data))
    return f


@pytest.fixture(scope='function')
def mock_os_api_get_projects():
    def f(r):
        if 'Authorization' not in r.headers:
            return (400, "", "Bad Request")
        path = osp.join(osp.dirname(osp.realpath(__file__)),
                        'mock_api_json_replies',
                        'os_get_projects.json')
        with open(path) as data_file:
            data = json.load(data_file)
        headers = {'r-id': '728d329e-0e86-11e4-a748-0c84dc037c13'}
        return (200, headers, json.dumps(data))
    return f
