import logging

from prometheus_flask_exporter import PrometheusMetrics

logger = logging.getLogger(__name__)

metrics = PrometheusMetrics(app=None)


def init_metrics(app, version):
    """
    Initialize metrics.
    """
    metrics.init_app(app)
    metrics.info('application', 'echo-roman', version=version)
