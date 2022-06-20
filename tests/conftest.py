import pytest
import os

from flaskr import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )

    f = open("REVISION", "a")
    f.write("aa603866")
    f.close()

    yield app

    os.remove("REVISION")

    # clean up / reset resources here


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
