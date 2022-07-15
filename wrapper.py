import os

from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from json_to_graphviz_svg import convert_json_to_graphviz_svg
from json_to_lex_repo import convert_json_to_lex_files
#from json_to_lex_repo import new_convert_json_to_lex_files

import sentry_sdk
sentry_sdk.init(
    dsn="https://4abd3e27fde7403595de41b8d7a626d6@o1318244.ingest.sentry.io/6575867",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)


app = Flask(__name__)
CORS(app)


@app.route("/convert_json_to_graphviz/", methods=['POST'])
def convert_json_to_graphviz():
    body = request.json
    svg = convert_json_to_graphviz_svg(body)
    response = make_response(jsonify(svg))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/convert_json_to_lex_repo/", methods=['POST'])
def convert_json_to_lex_repo():
    body = request.json
    convert_json_to_lex_files(body)
    data = {'message': 'Created', 'code': 'SUCCESS'}
    response = make_response(jsonify(data))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/new_convert_json_to_lex_repo/", methods=['POST'])
def new_convert_json_to_lex_repo():
    body = request.json
    #new_convert_json_to_lex_files(body)
    data = {'message': 'Created', 'code': 'SUCCESS'}
    response = make_response(jsonify(data))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
