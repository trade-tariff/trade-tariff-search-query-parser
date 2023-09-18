import logging
import json_logging


class NoHealth(logging.Filter):
    def filter(self, record):
        if hasattr(record, "request"):
            return "health" not in record.request

        return True


class LoggingConfigurator(object):
    def __init__(self, app):
        self._app = app

    def configure(self):
        if not json_logging.ENABLE_JSON_LOGGING:
            json_logging.init_flask(enable_json=True)
            json_logging.init_request_instrument(self._app)

            for handler in self._app.logger.handlers:
                handler.addFilter(NoHealth())

            for handler in logging.getLogger("json_logging").handlers:
                handler.addFilter(NoHealth())

            for handler in logging.getLogger("flask-request-logger").handlers:
                handler.addFilter(NoHealth())
