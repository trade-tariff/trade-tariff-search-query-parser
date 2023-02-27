import os
import pytest

from flaskr.synonym_file_handler import SynonymFileHandler


@pytest.fixture
def test_file_path():
    # Validates explicit and equivalent mappings as well as empty lines, whitespace and duplicate tokens
    file_contents = """abridgement, abridgment, capsule, condensation
abyssinian => cat, abyssinian
red lemon => bird
lemon => bird
red kite => alarming
red kite => bird
abridgement => abyssinian, cat
test=>spaces



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
    handler = SynonymFileHandler(test_file_path)
    expected_terms_to_tokens = {
        "abridgement": {
            "abyssinian",
            "cat",
            "condensation",
            "abridgement",
            "abridgment",
            "capsule",
        },
        "abridgment": {"abridgment", "capsule", "condensation", "abridgement"},
        "capsule": {"abridgment", "capsule", "condensation", "abridgement"},
        "condensation": {"abridgment", "capsule", "condensation", "abridgement"},
        "abyssinian": {"abyssinian", "cat"},
        "red lemon": {"bird"},
        "lemon": {"bird"},
        "red kite": {"alarming", "bird"},
        "test": {"spaces"},
    }
    assert handler.load() == expected_terms_to_tokens


def test_load_empty_file(test_empty_file_path):
    handler = SynonymFileHandler(test_empty_file_path)
    expected_terms_to_tokens = {}
    assert handler.load() == expected_terms_to_tokens


def test_load_with(test_file_path):
    with SynonymFileHandler(test_file_path) as terms_to_tokens:
        expected_terms_to_tokens = {
            "abridgement": {
                "abyssinian",
                "cat",
                "condensation",
                "abridgement",
                "abridgment",
                "capsule",
            },
            "abridgment": {"abridgment", "capsule", "condensation", "abridgement"},
            "capsule": {"abridgment", "capsule", "condensation", "abridgement"},
            "condensation": {"abridgment", "capsule", "condensation", "abridgement"},
            "abyssinian": {"abyssinian", "cat"},
            "red lemon": {"bird"},
            "lemon": {"bird"},
            "red kite": {"alarming", "bird"},
            "test": {"spaces"},
        }
        assert terms_to_tokens == expected_terms_to_tokens
