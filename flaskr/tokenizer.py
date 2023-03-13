import spacy
import os
from flaskr.stemming_exclusion_file_handler import StemmingExclusionFileHandler
from flaskr.quote_tokeniser import QuoteTokeniser

stemming_exclusion_handler = StemmingExclusionFileHandler()
stemming_exclusion_handler.load()
nlp = spacy.load(os.environ["SPACY_DICTIONARY"])


class Tokenizer:
    def __init__(self, search_query):
        self._search_query = search_query
        self._quoted_tokens = QuoteTokeniser.tokenise(search_query)
        self._debug_tokens = os.getenv("DEBUG_TOKENS") == "true"

    def get_tokens(self):
        quoted_tokens = []
        unquoted_tokens = []
        quoted_search_query = ""
        unquoted_search_query = ""

        for token, quoted in self._quoted_tokens:
            if quoted:
                quoted_search_query += token + " "
            else:
                unquoted_search_query += token + " "

        doc = nlp(unquoted_search_query)

        cleaned_chunks = self._clean_chunks(doc)
        cleaned_tokens = self._clean_tokens(doc)

        nouns = [self._handle_excluded_token(token) for token in cleaned_tokens if token.pos_ == "NOUN"]
        verbs = [self._handle_excluded_token(token) for token in cleaned_tokens if token.pos_ == "VERB"]
        adjectives = [self._handle_excluded_token(token) for token in cleaned_tokens if token.pos_ == "ADJ"]

        if quoted_search_query:
            quoted_search_query = quoted_search_query.strip()
            quoted_tokens += quoted_search_query.split(" ")

        if unquoted_search_query:
            unquoted_search_query = unquoted_search_query.strip()
            unquoted_tokens += unquoted_search_query.split(" ")

        tokens = {
            "quoted": quoted_tokens,
            "unquoted": unquoted_tokens,
            "nouns": nouns,
            "verbs": verbs,
            "adjectives": adjectives,
            "noun_chunks": cleaned_chunks,
        }

        if self._debug_tokens:
            self._record_token_information(tokens, doc)

        return tokens

    def _clean_chunks(self, doc):
        noun_chunks = list(doc.noun_chunks)
        clean_noun_chunks = []

        for chunk in noun_chunks:
            clean_tokens = [token for token in chunk if not token.is_punct]
            if clean_tokens:
                clean_text = ' '.join([token.text for token in clean_tokens])
            else:
                clean_text = chunk.text
            clean_noun_chunks.append(clean_text)

        return clean_noun_chunks


    def _handle_excluded_token(self, token):
        should_lemma = not token.text in stemming_exclusion_handler.excluded_terms

        if should_lemma:
            return token.lemma_
        else:
            return token.text

    def _clean_tokens(self, doc):
        return [token for token in doc if self._is_clean_token(token)]

    def _is_clean_token(self, token):
        dirty_token = token.is_stop or token.is_punct

        return not dirty_token



    def _record_token_information(self, tokens, doc):
        all_tokens = {}

        for token in doc:
            all_tokens[token.text] = {
                "lemma": token.lemma_,
                "pos": token.pos_,
                "tag": token.tag_,
                "dep": token.dep_,
                "shape": token.shape_,
                "is_alpha": token.is_alpha,
                "is_stop": token.is_stop,
                "is_punct": token.is_punct,
            }

        tokens["all"] = all_tokens
