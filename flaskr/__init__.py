import os

from flask import Flask

from flaskr import tokenizer
from flaskr import spelling_corrector as sc


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/tokens/<string:term>", methods=["GET"])
    def tokens(term):
        entities = tokenizer.get_entities(term)

        return {"entities": entities}

    @app.route("/healthcheck", methods=["GET"])
    def healthcheck():
        adjectives = tokenizer.get_entities("tall man")["tokens"]["adjectives"]
        healthy = adjectives == ["tall"]
        sha = open("REVISION").read().strip()

        healthcheck = {}
        healthcheck["git_sha1"] = sha
        healthcheck["healthy"] = healthy

        return healthcheck

    @app.route("/correct-words/<string:term>", methods=['GET'])
    def spelling_corrector(term):
        words = sc.correct(term)

        return { 'words': words }

    return app
