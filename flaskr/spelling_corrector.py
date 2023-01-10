import os
import re
import boto3
from botocore.exceptions import NoCredentialsError
from textblob.en import Spelling


class SpellingCorrector:
    SPELLING_MODEL_FILEPATH = "config/data/spelling-model.txt"
    SPELLING_MODEL_FALLBACK_FILEPATH = "config/data/spelling-model-fallback.txt"
    SPELLING_MODEL_OBJECT_PATH = "spelling-corrector/spelling-model.txt"

    def __init__(self, spelling):
        self._spelling = spelling

    def correct(self, term):
        words = re.findall(r"\w+", term)

        corrected_terms = []

        for word in words:
            corrected_term = self._spelling.suggest(word)[0][0]
            corrected_terms.append(corrected_term)

        return " ".join(corrected_terms)

    @classmethod
    def build(cls):
        spelling = Spelling(SpellingCorrector.SPELLING_MODEL_FALLBACK_FILEPATH)
        corrector = SpellingCorrector(spelling)

        SpellingCorrector.download_file()

        try:
            spelling = Spelling(SpellingCorrector.SPELLING_MODEL_FILEPATH)
            spelling.load()

            corrector = SpellingCorrector(spelling)
        except Exception:
            pass

        return corrector

    @classmethod
    def download_file(cls):
        if not os.getenv("FLASK_ENV") == "test":
            try:
                bucket_name = os.getenv("SPELLING_CORRECTOR_BUCKET_NAME")
                s3_client = boto3.client("s3")
                s3_client.download_file(
                    bucket_name,
                    SpellingCorrector.SPELLING_MODEL_OBJECT_PATH,
                    SpellingCorrector.SPELLING_MODEL_FILEPATH,
                )
            except NoCredentialsError:
                pass
