# -*- coding: utf-8 -*-
#
# This file is part of Kwek Metrics.

"""Kwek Metrics views."""

from .views import blueprint as main_blueprint
from .services import blueprint as service_blueprint

blueprints = [main_blueprint, service_blueprint]
