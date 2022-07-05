import os

from flask import Flask, request

from flaskr import tokenizer
from flaskr.spelling_corrector import SpellingCorrector


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Initialize Spelling Corrector

    spelling_train_path = os.path.join(app.root_path, "data", "spelling_train.txt")
    spell_corrector = SpellingCorrector(spelling_train_path)

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

    api_prefix = "/api/search"

    @app.route(f"{api_prefix}/tokens", methods=["GET"])
    def tokens():
        search_query = request.args.get("q", default="", type=str)

        if search_query == "":
            return "Error: the query params is empty.", 400

        corrected_search_query = spell_corrector.correct(search_query)

        result = {}
        result["original_search_query"] = search_query
        result["corrected_search_query"] = corrected_search_query

        tokens = tokenizer.get_tokens(corrected_search_query)
        result["tokens"] = tokens

        return result

    @app.route(f"{api_prefix}/healthcheck", methods=["GET"])
    def healthcheck():
        tokens = tokenizer.get_tokens("tall man")["all"]
        healthy = len(tokens) == 2
        sha = open("REVISION").read().strip()

        healthcheck = {}
        healthcheck["git_sha1"] = sha
        healthcheck["healthy"] = healthy

        return healthcheck

    return app
