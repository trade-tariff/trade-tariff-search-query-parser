import os
from flaskr import error_logging
from flask import Flask, request

from flaskr.tokenizer import Tokenizer
from flaskr.spelling_corrector import SpellingCorrector
from flaskr.synonym_file_handler import SynonymFileHandler
from flaskr.synonym_expander import SynonymExpander
from flaskr.stemming_exclusion_file_handler import StemmingExclusionFileHandler


def create_app(test_config=None):
    error_logging.setup_sentry()

    app = Flask(__name__, instance_relative_config=True)
    spell_corrector = SpellingCorrector()
    synonym_handler = SynonymFileHandler()
    synonym_handler.load()
    synonym_expander = SynonymExpander(synonym_handler.terms_to_tokens)

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

    # isolated healthcheck route
    @app.get("/healthcheckz")
    def healthz():
        json = {"message": "OK"}
        return json, 200

    api_prefix = "/api/search"

    @app.route(f"{api_prefix}/tokens", methods=["GET"])
    def tokens():
        search_query = request.args.get("q", default="", type=str)

        spell = request.args.get("spell", default="1", type=str) == "1"
        expand_synonyms = (
            request.args.get("expand_synonyms", default="1", type=str) == "1"
        )

        corrected_search_query = (
            spell_corrector.correct(search_query) if spell else search_query
        )

        expanded_search_query = (
            synonym_expander.expand(corrected_search_query)
            if expand_synonyms
            else corrected_search_query
        )

        result = {}
        result["original_search_query"] = search_query
        result["corrected_search_query"] = corrected_search_query
        result["expanded_search_query"] = expanded_search_query

        tokenizer = Tokenizer(expanded_search_query)
        tokens = tokenizer.get_tokens()

        result["tokens"] = tokens

        return result

    @app.route(f"{api_prefix}/healthcheck", methods=["GET"])
    def healthcheck():
        spell_corrector.load_spelling()
        synonym_handler.load()

        tokens = Tokenizer("tall man").get_tokens()
        healthy = tokens["adjectives"] == ["tall"]
        healthy = healthy and tokens["nouns"] == ["man"]

        using_spelling_fallback = (
            False
            if os.path.exists(path=SpellingCorrector.SPELLING_MODEL_FILEPATH)
            else True
        )
        using_synonym_fallback = (
            False if os.path.exists(path=SynonymFileHandler.SYNONYM_FILEPATH) else True
        )
        using_stemming_exclusion_fallback = (
            False if os.path.exists(path=StemmingExclusionFileHandler.STEMMING_EXCLUSION_FILEPATH) else True
        )

        sha = (
            open("REVISION").read().strip() if os.path.exists("REVISION") else "unknown"
        )

        healthcheck = {}
        healthcheck["git_sha1"] = sha
        healthcheck["healthy"] = healthy
        healthcheck["using_spelling_fallback"] = using_spelling_fallback
        healthcheck["using_synonym_fallback"] = using_synonym_fallback
        healthcheck["using_stemming_exclusion_fallback"] = using_stemming_exclusion_fallback

        return healthcheck

    return app
