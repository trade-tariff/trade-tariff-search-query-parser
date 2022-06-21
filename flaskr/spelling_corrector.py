import re
from textblob.en import Spelling


class SpellingCorrector:
    def __init__(self, spelling_train_path):
        self.spelling = Spelling(path=spelling_train_path)

    def correct(self, term):
        words = re.findall(r"\w+", term)

        corrected_terms = []

        for word in words:
            corrected_term = self.spelling.suggest(word)[0][0]
            corrected_terms.append(corrected_term)

        return corrected_terms
