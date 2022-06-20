import re
import os
from textblob.en import Spelling

class SpellingCorrector:
    def __init__(self, app):
        path = os.path.join(app.root_path, "data", "spelling_train.txt")
        self.spelling = Spelling(path=path)

    def correct(self, term):
        words = re.findall(r'\w+', term)

        corrected_terms = []

        for word in words:
            corrected_term = self.spelling.suggest(word)[0][0]
            corrected_terms.append(corrected_term)

        return corrected_terms
