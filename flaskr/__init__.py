import os
from flaskr import error_logging
from flask import Flask, request

from flaskr import tokenizer
from flaskr.spelling_corrector import SpellingCorrector


def create_app(test_config=None):
    error_logging.setup_sentry()

    app = Flask(__name__, instance_relative_config=True)
    spell_corrector = SpellingCorrector()

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
        spell = request.args.get("spell", default="1", type=str) == "1"
        corrected_search_query = (
            spell_corrector.correct(search_query) if spell else search_query
        )

        result = {}
        result["original_search_query"] = search_query
        result["corrected_search_query"] = corrected_search_query

        tokens = tokenizer.get_tokens(corrected_search_query)
        result["tokens"] = tokens

        return result

    @app.route(f"{api_prefix}/healthcheck", methods=["GET"])
    def healthcheck():
        spell_corrector.load_spelling()

        tokens = tokenizer.get_tokens("tall man")["all"]
        healthy = len(tokens) == 2
        using_fallback = (
            False
            if os.path.exists(path=SpellingCorrector.SPELLING_MODEL_FILEPATH)
            else True
        )
        sha = (
            open("REVISION").read().strip() if os.path.exists("REVISION") else "unknown"
        )

        healthcheck = {}
        healthcheck["git_sha1"] = sha
        healthcheck["healthy"] = healthy
        healthcheck["using_fallback"] = using_fallback

        return healthcheck

    return app
