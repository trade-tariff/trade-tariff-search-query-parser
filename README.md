# trade-tariff-search-query-parser
The main goal of this Flask App is to parse the search term queries the users type on Trade Tarif find_commodity page.

## Installation

### Create local env:
```
python3 -m venv venv
```

### Activate the environment

```
. ./venv/bin/activate
```

### Install the requirements

```
pip install -r requirements.txt
```

## Run Flask Server
set FLASK_ENV var

export FLASK_ENV=development

```
flask run
```

## How to run tests
This project uses [pytest](https://docs.pytest.org/), to run all the tests just run:

```
pytest
```

or you can specify the test file you to run:

```
pytest file_or_dir
```
