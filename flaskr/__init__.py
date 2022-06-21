import os

from flask import Flask

from flaskr import tokenizer
from flaskr import spelling_corrector


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Initialize Spelling Corrector

    spelling_train_path = os.path.join(app.root_path, "data", "spelling_train.txt")
    spell_corr = spelling_corrector.SpellingCorrector(spelling_train_path)

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

    api_prefix = "/api/search/"

    @app.route(f"{api_prefix}/tokens/<string:term>", methods=["GET"])
    def tokens(term):
        entities = tokenizer.get_entities(term)

        return {"entities": entities}

    @app.route(f"{api_prefix}/healthcheck", methods=["GET"])
    def healthcheck():
        tokens = tokenizer.get_entities("tall man")["tokens"]["all"]
        healthy = len(tokens) == 2
        sha = open("REVISION").read().strip()

        healthcheck = {}
        healthcheck["git_sha1"] = sha
        healthcheck["healthy"] = healthy

        return healthcheck

    @app.route(f"{api_prefix}/correct-terms/<string:term>", methods=["GET"])
    def correct_terms(term):
        corrected_terms = spell_corr.correct(term)

        return {
            "entities": {"correct_terms": corrected_terms, "original_terms": term},
        }

    return app
