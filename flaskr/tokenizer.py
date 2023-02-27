import spacy
import os

nlp = spacy.load(os.environ["SPACY_DICTIONARY"])


class Tokenizer:
    def __init__(self):
        pass

    def get_tokens(self, search_query):
        doc = nlp(search_query)

        all_tokens = [token.lemma_ for token in doc]

        tokens = {
            "all": all_tokens,
            "nouns": [token.lemma_ for token in doc if token.pos_ == "NOUN"],
            "verbs": [token.lemma_ for token in doc if token.pos_ == "VERB"],
            "adjectives": [token.lemma_ for token in doc if token.pos_ == "ADJ"],
            "noun_chunks": [chunk.text for chunk in doc.noun_chunks],
        }

        return tokens
