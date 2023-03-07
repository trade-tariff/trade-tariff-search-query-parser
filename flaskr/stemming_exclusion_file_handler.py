import os
import boto3
from botocore.exceptions import NoCredentialsError

"""
Converts stemming exclusion files into a dictionary of terms to tokens which can be used
to prevent lemmatization of certain terms.

Parameters:
    filename (str): The path to the stemming_exclusion file.

Returns:
    dict: A dictionary of terms to tokens.
"""


class StemmingExclusionFileHandler:
    STEMMING_EXCLUSION_FILEPATH = "config/data/stemming-exclusions-all.txt"
    STEMMING_EXCLUSION_FALLBACK_FILEPATH = "config/data/stemming-exclusions-all-fallback.txt"
    STEMMING_EXCLUSION_OBJECT_PATH = "config/opensearch/stemming_exclusions_all.txt"

    def __init__(self, filename=None):
        self.filename = filename
        self.excluded_terms = set()

    def load(self):
        self.download_file()
        self.parse_file()

        return self.excluded_terms

    def download_file(self):
        if not os.getenv("FLASK_ENV") == "test":
            try:
                bucket_name = os.getenv("PACKAGE_BUCKET_NAME") or ""
                s3_client = boto3.client("s3")
                s3_client.download_file(
                    bucket_name,
                    StemmingExclusionFileHandler.STEMMING_EXCLUSION_OBJECT_PATH,
                    StemmingExclusionFileHandler.STEMMING_EXCLUSION_FILEPATH,
                )
            except NoCredentialsError:
                pass

    def parse_file(self):
        if self.filename:
            filename = self.filename
        elif os.path.exists(StemmingExclusionFileHandler.STEMMING_EXCLUSION_FILEPATH):
            filename = StemmingExclusionFileHandler.STEMMING_EXCLUSION_FILEPATH
        else:
            filename = StemmingExclusionFileHandler.STEMMING_EXCLUSION_FALLBACK_FILEPATH

        with open(filename, "r") as f:
            stemming_exclusion_lines = f.read().splitlines()

            for line in stemming_exclusion_lines:
                if not line:
                    continue
                else:
                    lhs, rhs = (
                        [r.strip() for r in line.split("=>")]
                        if "=>" in line
                        else (line, None)
                    )

                    if lhs and rhs:
                        if lhs == rhs:
                            terms = [t.strip() for t in lhs.split(",")]

                            for term in terms:
                                self.excluded_terms.add(term)

    def __enter__(self):
        return self.load()

    def __exit__(self, exc_type, exc_value, traceback):
        pass
