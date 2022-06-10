import spacy

nlp = spacy.load("en_core_web_sm")

def get_entities(term):
    doc = nlp(term)

    entities = {}

    entities["tokens"] = {
        "all": [token.lemma_ for token in doc],
        "nouns": [token.lemma_ for token in doc if token.pos_ == "NOUN"],
        "verbs": [token.lemma_ for token in doc if token.pos_ == "VERB"],
        "adjectives": [token.lemma_ for token in doc if token.pos_ == "ADJ"]
    }

    entities["noun_chunks"] = [chunk.text for chunk in doc.noun_chunks]

    return entities
