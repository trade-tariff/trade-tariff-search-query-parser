import os

os.environ["FLASK_ENV"] = "test"
os.environ["SPACY_DICTIONARY"] = "en_core_web_sm"
os.environ["EXPAND_EXPLICIT_SYNONYMS"] = "true"
os.environ["EXPAND_EQUIVALENT_SYNONYMS"] = "true"
