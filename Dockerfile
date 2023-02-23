FROM python:3.11-slim-bullseye

WORKDIR /app

COPY requirements.txt requirements.txt
COPY requirements/ requirements/

RUN apt-get update \
  && apt-get install --assume-yes --quiet curl gcc \
  && apt-get clean \
  && pip install --no-cache-dir -r requirements.txt

RUN python -m spacy download en_core_web_md

COPY . .

ENV FLASK_ENV=production
ENV FLASK_APP=flaskr
ENV SPACY_DICTIONARY=en_core_web_md
CMD ["waitress-serve", "--call", "flaskr:create_app"]
