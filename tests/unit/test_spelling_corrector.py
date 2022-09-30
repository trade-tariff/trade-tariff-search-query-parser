import os
from flaskr.spelling_corrector import SpellingCorrector


def test_spelling_corrector_correct(app):
    spelling_train_path = os.path.join(app.root_path, "data", "spelling-model.txt")
    spell_corrector = SpellingCorrector(spelling_train_path)
    search_query = "halbiut sausadge stenolepsis chese bnoculars parnsip farmacy pape"
    corrected_search_query = spell_corrector.correct(search_query)

    assert (
        corrected_search_query
        == "halibut sausage stenolepis cheese binoculars parsnip pharmacy paper"
    )
