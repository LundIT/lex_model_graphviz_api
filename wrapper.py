import os
import traceback

from flask import Flask, request

from json_to_graphviz_svg import convert_json_to_graphviz_svg
from json_to_lex_repo import convert_json_to_lex_files

app = Flask(__name__)

@app.route("/convert_json_to_graphviz/", methods = ['POST'])
def convert_json_to_graphviz_svg_route():
    body = request.json
    svg = convert_json_to_graphviz_svg(body)
    return svg

@app.route("/convert_json_to_lex_repo/", methods = ['POST'])
def convert_json_to_lex_repo_route():
    body = request.json
    try:
        convert_json_to_lex_files(body)
    except Exception as e:
        print(traceback.print_exc())
        return {'success': False, 'error_message':f"Error: Creating Documents failed with Exception {str(e)}", 'traceback': traceback.print_exc()}
    return {'success': True}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))