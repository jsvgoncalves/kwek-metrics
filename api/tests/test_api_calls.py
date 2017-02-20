# -*- coding: utf-8 -*-
#
# This file is part of Kwek Metrics.
import responses

from api.hawkular import query_api
from api.hawkular import get_metric
from api.hawkular import get_os_projects

METRICS_URL = 'https://metrics-url.com/'
OS_URL = 'https://os-url.com/'


def test_generic_api_call():
    with responses.RequestsMock() as rsps:
        # Mock
        rsps.add(responses.GET,
                 METRICS_URL,
                 body='{"got": "this"}', status=200,
                 content_type='application/json')
        # Test
        resp = query_api(METRICS_URL)
        assert resp is not None
        assert resp.json() == {'got': 'this'}

        assert len(rsps.calls) == 1
        assert rsps.calls[0].request.url == METRICS_URL
        assert rsps.calls[0].response.text == '{"got": "this"}'


def test_getting_user_projects(mock_os_api_get_projects):
    """Tests getting a response with four projects.

    Args:
        mock_os_api_get_projects (mock): mock method for the API Call

    """
    with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps:
        # Mock
        rsps.add_callback(
            responses.GET,
            OS_URL,
            callback=mock_os_api_get_projects)

        # Test
        # This data comes from elsewhere
        url = OS_URL
        auth = 'XXXX'
        resp = get_os_projects(url, auth)

        assert len(resp) == 4
        assert resp[0]['metadata']['name'] is not None


def test_get_hawkular_metric_from_namespace(mock_hawkular_api):
    with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps:
        # Mock
        rsps.add_callback(
            responses.GET, METRICS_URL,
            callback=mock_hawkular_api
        )

        # Test
        # This data comes from elsewhere..
        metric = 'cpu%2Fusage_rate'
        tenant = '_tenant'
        auth = 'XXXX'
        url = METRICS_URL
        resp = get_metric(url, tenant, auth, metric)

        assert resp is not None
        assert len(resp) >= 1


def test_aggregating_metrics():
    """Test getting metrics from multiple namespaces and aggregating them
    """
    pass
