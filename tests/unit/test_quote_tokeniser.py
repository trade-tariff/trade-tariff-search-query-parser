from flaskr.quote_tokeniser import QuoteTokeniser


def test_tokenise_single_quotes():
    query = "this is a 'test query'"
    tokeniser = QuoteTokeniser()
    expected = [
        ('this', False),
        ('is', False),
        ('a', False),
        ('\'test query\'', True),
    ]

    actual = tokeniser.tokenise(query)

    assert actual == expected

def test_tokenise_double_quotes():
    query = 'this is a "test query"'
    tokeniser = QuoteTokeniser()
    expected = [
        ('this', False),
        ('is', False),
        ('a', False),
        ('"test query"', True),
    ]
    actual = tokeniser.tokenise(query)

    assert actual == expected

def test_tokenise_mixed_quotes():
    query = 'this is a "test query" and this is a \'test query\''
    tokeniser = QuoteTokeniser()
    expected = [
        ('this', False),
        ('is', False),
        ('a', False),
        ('"test query"', True),
        ('and', False),
        ('this', False),
        ('is', False),
        ('a', False),
        ('\'test query\'', True),
    ]
    actual = tokeniser.tokenise(query)

    assert actual == expected

def test_tokenise_empty_string():
    query = ''
    tokeniser = QuoteTokeniser()
    expected = []
    actual = tokeniser.tokenise(query)

    assert actual == expected

def test_tokenise_none():
    query = None
    tokeniser = QuoteTokeniser()
    expected = []
    actual = tokeniser.tokenise(query)

    assert actual == expected

def test_tokenise_incomplete_double_quotes():
    query = 'this is a "test query'
    tokeniser = QuoteTokeniser()
    expected = [
        ('this', False),
        ('is', False),
        ('a', False),
        ('"test', False),
        ('query', False),
    ]
    actual = tokeniser.tokenise(query)

    assert actual == expected

def test_tokenise_incomplete_single_quotes():
    query = 'this is a \'test query'
    tokeniser = QuoteTokeniser()
    expected = [
        ('this', False),
        ('is', False),
        ('a', False),
        ('\'test', False),
        ('query', False),
    ]
    actual = tokeniser.tokenise(query)

    assert actual == expected
