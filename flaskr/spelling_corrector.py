import re
import os
from textblob.en import Spelling
from flask import current_app as app

def correct(term):
    pathToFile = os.path.join(app.root_path, "data", "spelling_train.txt")
    spelling = Spelling(path=pathToFile)

    words = re.findall(r'\w+', term)

    corrected_terms = []

    for word in words:
        print(spelling.suggest(word))
        corrected_term = spelling.suggest(word)[0][0]
        corrected_terms.append(corrected_term)

        filename = os.path.join(app.instance_path, 'my_folder')

    return corrected_terms
