import os

from flask import Flask

from flaskr import tokenizer
from flaskr import spelling_corrector


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Initialize Spelling Corrector
    spell_corr = spelling_corrector.SpellingCorrector(app)

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

    @app.route("/correct-terms/<string:term>", methods=['GET'])
    def correct_terms(term):
        corrected_terms = spell_corr.correct(term)

        return {
                'entities': {
                    'correct_terms': corrected_terms,
                    'original_terms': term
                    },
                }

    return app
