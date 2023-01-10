from flaskr.spelling_corrector import SpellingCorrector


def test_spelling_corrector_correct():
    spelling_corrector = SpellingCorrector.build()
    search_query = "halbiut sausadge stenolepsis chese bnoculars parnsip farmacy papre"
    corrected_search_query = spelling_corrector.correct(search_query)

    assert (
        corrected_search_query
        == "halibut sausage stenolepis cheese binoculars parsnip pharmacy paper"
    )


def test_spelling_corrector_synonym_not_corrected():
    spelling_corrector = SpellingCorrector.build()
    search_query = "acamol"
    corrected_search_query = spelling_corrector.correct(search_query)

    assert corrected_search_query == "acamol"
