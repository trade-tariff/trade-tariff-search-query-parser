import os
import boto3
from botocore.exceptions import NoCredentialsError

EXPAND_EQUIVALENT_SYNONYMS = os.getenv("EXPAND_EQUIVALENT_SYNONYMS") == "true"
EXPAND_EXPLICIT_SYNONYMS = os.getenv("EXPAND_EXPLICIT_SYNONYMS") == "true"

"""
Converts synonym files into a dictionary of terms to tokens which can be used to expand queries
into a set of equivalent synonym tokens. Handles empty lines, whitespace, and duplicate tokens as well as equivalent
mappings (e.g. "abyssinian => cat, abyssinian") and explicit mappings (e.g. "abridgement, abridgment, capsule,
condensation").

Parameters:
    filename (str): The path to the synonym file.

Returns:
    dict: A dictionary of terms to tokens.
"""


class SynonymFileHandler:
    SYNONYM_FILEPATH = "config/data/synonyms-all.txt"
    SYNONYM_FALLBACK_FILEPATH = "config/data/synonyms-all-fallback.txt"
    SYNONYM_OBJECT_PATH = "config/opensearch/synonyms_all.txt"

    def __init__(self, filename=None):
        self.filename = filename
        self.terms_to_tokens = {}

    def load(self):
        self.download_file()
        self.parse_file()

        return self.terms_to_tokens

    def download_file(self):
        if not os.getenv("FLASK_ENV") == "test":
            try:
                bucket_name = os.getenv("SYNONYM_PACKAGE_BUCKET_NAME") or ""
                s3_client = boto3.client("s3")
                s3_client.download_file(
                    bucket_name,
                    SynonymFileHandler.SYNONYM_OBJECT_PATH,
                    SynonymFileHandler.SYNONYM_FILEPATH,
                )
            except NoCredentialsError:
                pass

    def parse_file(self):
        if self.filename:
            filename = self.filename
        elif os.path.exists(SynonymFileHandler.SYNONYM_FILEPATH):
            filename = SynonymFileHandler.SYNONYM_FILEPATH
        else:
            filename = SynonymFileHandler.SYNONYM_FALLBACK_FILEPATH

        with open(filename, "r") as f:
            synonym_lines = f.read().splitlines()

            for line in synonym_lines:
                if not line:
                    continue
                else:
                    lhs, rhs = (
                        [r.strip() for r in line.split("=>")]
                        if "=>" in line
                        else (line, None)
                    )

                    # Explicit mappings
                    if rhs and EXPAND_EXPLICIT_SYNONYMS:
                        terms = [t.strip() for t in lhs.split(",")]
                        tokens = [r.strip() for r in rhs.split(",")]
                        for term in terms:
                            if term in self.terms_to_tokens:
                                union = self.terms_to_tokens[term].union(set(tokens))
                                self.terms_to_tokens[term] = union
                            else:
                                self.terms_to_tokens[term] = set(tokens)
                    # Equivalent mappings
                    elif lhs and EXPAND_EQUIVALENT_SYNONYMS:
                        tokens = [r.strip() for r in lhs.split(",")]
                        terms = tokens
                        for term in terms:
                            if term in self.terms_to_tokens:
                                union = self.terms_to_tokens[term].union(set(tokens))
                                self.terms_to_tokens[term] = union
                            else:
                                self.terms_to_tokens[term] = set(tokens)

    def __enter__(self):
        return self.load()

    def __exit__(self, exc_type, exc_value, traceback):
        pass
