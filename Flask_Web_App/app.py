from flask import Flask, jsonify, request
import sys, os
sys.path.append(os.getcwd()+'/sample')
from sample import Sample
import json
app = Flask(__name__)


@app.route("/", methods=['GET'])
def hello():
    return "Hello World"


@app.route('/reply', methods=['GET'])
def reply():
    return "reply"


@app.route('/sample', methods=['GET'])
def sample():
    sam = Sample()
    return sam.print_str()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
