# -*- coding: utf-8 -*-
#
# Joao Goncalves
import requests
# import api.constants as cfg
# from urllib.parse import urljoin
# PROJECTS_URL = urljoin(cfg.OS_URL, 'todos')
# PROJECTS_URL = cfg.OS_URL + 'projects'
import json


class HawkularAPIError(Exception):
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        super(HawkularAPIError, self).__init__(message)


def _build_hawkular_headers(tentant="", auth=""):
    """Generate the headers to access the API with successful auth.

    {'Hawkular-Tenant': '_tenant_name',
     'Accept': 'application/json',
     'Authorization': 'Bearer XXXX'}

    Args:
        tentant (str): The tenant which to query
        auth (str): The authorization token

    Returns:
        dict: A dict with formatted headers
    """
    return{
        'Hawkular-Tenant': "{0}".format(tentant),
        'Accept': 'application/json',
        'Authorization': 'Bearer {0}'.format(auth)
    }


def _build_hawkular_payload(metric):
    """Generate the payload for the current select metric.

    {'tags': 'descriptor_name:memory%2Fusage',
     'bucketDuration': '60000ms',
     'start': '-15mn',
     'stacked': 'true'}

    Args:
        metric (str): The string describing the metric on the API

    Returns:
        dict: A dict with formatted payload
    """
    return{
        'tags': 'descriptor_name:{0}'.format(metric),
        'bucketDuration': '60000ms',
        'start': '-15mn',
        'stacked': 'true'
    }


def get_metric(url, tenant, auth, metric):
    headers = _build_hawkular_headers(tenant, auth)
    payload = _build_hawkular_payload(metric)
    r = query_api(url, headers, payload)
    try:
        return json.loads(r.text)
    except ValueError as err:
        raise ValueError(err.message, {'response': r.text})


def _build_os_headers(auth=""):
    """Generate the headers to access the API with successful auth.

    {'Hawkular-Tenant': '_tenant_name',
     'Accept': 'application/json',
     'Authorization': 'Bearer XXXX'}

    Args:
        tentant (str): The tenant which to query
        auth (str): The authorization token

    Returns:
        dict: A dict with formatted headers
    """
    return{
        'Authorization': 'Bearer {0}'.format(auth)
    }


def get_os_projects(url, auth):
    headers = _build_os_headers(auth)
    r = query_api(url, headers)
    try:
        return json.loads(r.text)['items']
    except ValueError as err:
        raise ValueError(err.message, {'response': r.text})


def query_api(url, headers={}, payload={}):
    """Perfoms a GET request.

    Args:
        url (str): The url to perfom the GET
        headers (dict, optional): The headers for the request
        payload (dict, optional): The payload for the request

    Returns:
        Request: The Request object
    """
    r = requests.get(url, headers=headers, verify=False, params=payload)
    return r
