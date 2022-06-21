FROM python:3.10.5-slim-bullseye

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt \
  && apt-get update \
  && apt-get install --assume-yes --quiet curl \
  && apt-get clean


# Install the spacy English dictionary
RUN python -m spacy download en_core_web_sm

COPY . .

ENV FLASK_ENV=production
ENV FLASK_APP=flaskr
CMD ["waitress-serve", "--call", "flaskr:create_app"]
