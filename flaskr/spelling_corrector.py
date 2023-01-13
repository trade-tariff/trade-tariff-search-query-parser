import os
import re
import boto3
from botocore.exceptions import NoCredentialsError
from textblob.en import Spelling


class SpellingCorrector:
    SPELLING_MODEL_FILEPATH = "config/data/spelling-model.txt"
    SPELLING_MODEL_FALLBACK_FILEPATH = "config/data/spelling-model-fallback.txt"
    SPELLING_MODEL_OBJECT_PATH = "spelling-corrector/spelling-model.txt"

    def __init__(self):
        self._spelling = None

    def correct(self, term):
        self.load_spelling()

        words = re.findall(r"\w+", term)

        corrected_terms = []

        for word in words:
            corrected_term = self._spelling.suggest(word)[0][0]
            corrected_terms.append(corrected_term)

        return " ".join(corrected_terms)

    def load_spelling(self):
        if not self._spelling:
            spelling = Spelling(SpellingCorrector.SPELLING_MODEL_FALLBACK_FILEPATH)

            self.download_file()

            if os.path.exists(SpellingCorrector.SPELLING_MODEL_FILEPATH):
                try:
                    spelling = Spelling(SpellingCorrector.SPELLING_MODEL_FILEPATH)
                except Exception:
                    pass

            self._spelling = spelling

    def download_file(self):
        if not os.getenv("FLASK_ENV") == "test":
            try:
                bucket_name = os.getenv("SPELLING_CORRECTOR_BUCKET_NAME") or ""
                s3_client = boto3.client("s3")
                s3_client.download_file(
                    bucket_name,
                    SpellingCorrector.SPELLING_MODEL_OBJECT_PATH,
                    SpellingCorrector.SPELLING_MODEL_FILEPATH,
                )
            except NoCredentialsError:
                pass
