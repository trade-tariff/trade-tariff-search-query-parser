FROM python:3.11-slim-bullseye

WORKDIR /app

RUN apt-get update \
    && apt-get install --assume-yes --no-install-recommends --quiet curl gcc \
    && apt-get clean

COPY requirements.txt requirements.txt
COPY requirements/ requirements/
RUN pip install --no-cache-dir -r requirements.txt

RUN python -m spacy download en_core_web_md

COPY . .

ENV FLASK_ENV=production \
    FLASK_APP=flaskr \
    SPACY_DICTIONARY=en_core_web_md \
    PORT=8080

RUN addgroup --system tariff && \
    adduser --system --ingroup tariff tariff && \
    chown -R tariff:tariff /app

HEALTHCHECK CMD nc -z localhost $PORT

USER tariff

CMD waitress-serve --port $PORT --call flaskr:create_app
