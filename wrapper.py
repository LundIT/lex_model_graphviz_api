import os

from flask import Flask, request

from json_to_graphviz_svg import convert_json_to_graphviz_svg

app = Flask(__name__)

@app.route("/")
def default():
    body = request.json
    svg = convert_json_to_graphviz_svg(body)
    return svg

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))