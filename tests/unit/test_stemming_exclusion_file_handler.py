import os
import pytest

from flaskr.stemming_exclusion_file_handler import StemmingExclusionFileHandler


@pytest.fixture
def test_file_path():
    file_contents = """
clothing => clothing
whiting => whiting
cloth => cloth
"""
    test_file_path = "test_synonyms.csv"
    with open(test_file_path, "w") as f:
        f.write(file_contents)

    yield test_file_path
    # Remove the test synonym file
    os.remove(test_file_path)


@pytest.fixture
def test_empty_file_path():
    file_contents = ""
    test_file_path = "test_empty_synonyms.csv"
    with open(test_file_path, "w") as f:
        f.write(file_contents)

    yield test_file_path
    # Remove the test synonym file
    os.remove(test_file_path)


def test_load(test_file_path):
    handler = StemmingExclusionFileHandler(test_file_path)
    actual = handler.load()
    expected = {'whiting', 'cloth', 'clothing'}

    assert actual == expected


def test_load_empty_file(test_empty_file_path):
    handler = StemmingExclusionFileHandler(test_empty_file_path)
    actual = handler.load()
    expected = set()
    assert actual == expected
