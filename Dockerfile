FROM python:3.10.5-slim-bullseye

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# Install the spacy English dictionary
RUN python -m spacy download en_core_web_sm

COPY . .

ENV FLASK_ENV=production
ENV FLASK_APP=flaskr

CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
