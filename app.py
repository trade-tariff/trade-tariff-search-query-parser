from flask import Flask

app = Flask(__name__)

@app.route("/tokens/<string:term>", methods=['GET'])
def tokens(term):
    tokens = term.split()

    return { 'tokens': tokens }
