import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration


def setup_sentry():
    sentry_sdk.init(
        integrations=[
            FlaskIntegration(),
        ]
    )
