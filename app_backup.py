# from flask import Flask
# import sys
# sys.path.append('./src/')
# import tokenizer

# app = Flask(__name__)

# @app.route("/tokens/<string:term>", methods=['GET'])
# def tokens(term):
#     entities = tokenizer.get_entities(term)

#     return { 'entities': entities }
