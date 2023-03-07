import spacy
import os
from flaskr.stemming_exclusion_file_handler import StemmingExclusionFileHandler

stemming_exclusion_handler = StemmingExclusionFileHandler()
stemming_exclusion_handler.load()
nlp = spacy.load(os.environ["SPACY_DICTIONARY"])


class Tokenizer:
    def __init__(self):
        pass

    def get_tokens(self, search_query):
        doc = nlp(search_query)

        all_tokens = [self._handle_excluded_token(token) for token in doc]

        tokens = {
            "all": all_tokens,
            "nouns": [self._handle_excluded_token(token) for token in doc if token.pos_ == "NOUN"],
            "verbs": [self._handle_excluded_token(token) for token in doc if token.pos_ == "VERB"],
            "adjectives": [self._handle_excluded_token(token) for token in doc if token.pos_ == "ADJ"],
            "noun_chunks": [chunk.text for chunk in doc.noun_chunks],
        }

        return tokens

    def _handle_excluded_token(self, token):
        if token.text in stemming_exclusion_handler.excluded_terms:
            return token.text
        else:
            return token.lemma_
