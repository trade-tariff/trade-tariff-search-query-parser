# trade-tariff-search-query-parser

The main goal of this Flask App is to parse the search term queries the users type on Trade Tarif find_commodity page.

### Create local env

```bash
python -m venv venv
```

### Activate the environment

```bash
. ./venv/bin/activate
```

### Install the requirements

```bash
pip install -r requirements.txt
spacy download en_core_web_sm
```

### Run Flask Server

```bash
export SPACY_DICTIONARY=en_core_web_sm
export FLASK_ENV=development
export FLASK_APP=flaskr
flask run
```

### How to run tests

This project uses [pytest](https://docs.pytest.org/), to run all the tests just run:

```bash
pytest
```

or you can specify the test file you to run:

```bash
pytest path/to/file_or_dir
```
