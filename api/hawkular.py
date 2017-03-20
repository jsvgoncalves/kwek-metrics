# -*- coding: utf-8 -*-
#
# This file is part of Kwek Metrics.

"""Hawkular API calls."""
import json

import requests
from requests import ConnectionError

from api import DISABLE_WARNINGS

if DISABLE_WARNINGS:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class HawkularAPIError(Exception):
    """Custom Exception type for API Errors.
    """

    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(HawkularAPIError, self).__init__(message)


class APIAuthorizationError(Exception):
    """Used in case of 401 request status."""
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(APIAuthorizationError, self).__init__(message)


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
        'Authorization': 'Bearer {0}'.format(auth),
        'Content-Type': 'application/json'
    }


def _build_hawkular_payload(metric):
    """Generate the payload for the current select metric.

    {'tags': 'descriptor_name:memory/usage',
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


def _build_hawkular_tags_payload(tags, metric_type):
    """Generate the payload for the current select metric.

    Example:
    {'tags': 'descriptor_name:memory/usage|cpu/usage_rate',
     'buckets': '1',
     'type': 'pod_container'
    }

    Args:
        tags (list): The string describing the metric on the API
        metric_type (str): The "type" for the payload, either
            "pod" or "pod_container"

    Returns:
        dict: A dict with formatted payload
    """
    return{
        'buckets': '1',
        'tags': 'descriptor_name:{},type:{}'.format(
            '|'.join(tags),
            metric_type)
    }


def get_metric(url, tenant, auth, metric):
    """Get a metric dataset from Hawkular API.

    Args:
        url (str): The Hawkular endpoint to query
        tenant (str): The tenant with which to authenticate
        auth (str): The token for authentication
        metric (str): The desired metric

    Returns:
        str: The text from the processed request

    Raises:
        err: (ValueError, ConnectionError)
    """
    headers = _build_hawkular_headers(tenant, auth)
    payload = _build_hawkular_payload(metric)
    try:
        r = query_api(url, headers, payload)
        return json.loads(r.text)
    except (ValueError, ConnectionError) as err:
        raise err


def get_metrics(url, tenant, auth, tags, pod_selectors='pod'):
    """Get multiple metrics datasets from Hawkular API.

    Args:
        url (str): The Hawkular endpoint to query
        tenant (str): The tenant with which to authenticate
        auth (str): The token for authentication
        tags (list): The tags to query the endpoint
        pod_selectors (str, optional): The "type" for the payload,
            either "pod" or "pod_container"

     Returns:
        str: The text from the processed request

    Raises:
        err: (ValueError, ConnectionError)
    """
    headers = _build_hawkular_headers(tenant, auth)
    payload = _build_hawkular_tags_payload(tags, pod_selectors)
    try:
        r = query_api_post(url, headers, payload)
        return json.loads(r.text)
    except (ValueError, ConnectionError) as err:
        raise err


def _build_os_headers(auth=""):
    """Generate the headers to access the API with successful auth.

    {'Hawkular-Tenant': '_tenant_name',
     'Accept': 'application/json',
     'Authorization': 'Bearer XXXX'}

    Args:
        auth (str): The authorization token

    Returns:
        dict: A dict with formatted headers
    """
    return{
        'Authorization': 'Bearer {0}'.format(auth)
    }


def get_os_projects(url, auth):
    """Get the visible OpenShift projects from OpenShift API.

    Args:
        url (str): The endpoint of OpenShift API
        auth (str): The token to authenticate

    Returns:
        str: The JSON formatted text of the available projects

    Raises:
        err: (ValueError, ConnectionError)
    """
    headers = _build_os_headers(auth)
    try:
        r = query_api(url, headers)
        return json.loads(r.text)['items']
    except (ValueError, ConnectionError) as err:
        raise err


def query_api(url, headers={}, payload={}):
    """Perfoms a GET request.

    Args:
        url (str): The url to perfom the GET
        headers (dict, optional): The headers for the request
        payload (dict, optional): The payload for the request

    Returns:
        Request: The Request object

    Raises:
        ConnectionError: raised by requests.get()
        APIAuthorizationError: in case the API returns 401 Unauthorized
    """
    try:
        r = requests.get(url, headers=headers, verify=False, params=payload)
        if r.status_code == 401:
            raise APIAuthorizationError('Unauthorized')
        return r
    except ConnectionError as err:
        raise err


def query_api_post(url, headers={}, payload={}):
    """Perfoms a GET request.

    Args:
        url (str): The url to perfom the GET
        headers (dict, optional): The headers for the request
        payload (dict, optional): The payload for the request

    Returns:
        Request: The Request object

    Raises:
        err: ConnectionError raised by requests.get()
    """
    try:
        r = requests.post(url, headers=headers, verify=False, json=payload)
        if r.status_code == 401:
            raise APIAuthorizationError('Unauthorized')
        return r
    except ConnectionError as err:
        raise err
