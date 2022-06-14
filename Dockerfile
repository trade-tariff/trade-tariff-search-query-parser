FROM python:3.10.5

# TODO: if possible use the Alpine distribution
# FROM python:3.10.5-alpine3.16

WORKDIR /trade-tariff-search-query-parser

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

# Install the spaCy English dictionary
RUN python -m spacy download en_core_web_sm

COPY . .

ENV FLASK_ENV=development
ENV FLASK_APP=flaskr

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
