from flask import Flask, jsonify, request
import sys, os
sys.path.append(os.getcwd()+'/sample')
from sample import Sample
import json
app = Flask(__name__)


@app.route("/", methods=['GET'])
def hello():
    return "BitBank"


@app.route('/reply', methods=['GET'])
def reply():
    data = json.loads(request.data)
    answer = "Yes, it is %s!\n" % data["keyword"]
    result = {
      "Content-Type": "application/json",
      "Answer":{"Text": answer}
    }
    # return answer
    return "reply"


@app.route('/sample', methods=['GET'])
def sample():
    sam = Sample()
    return sam.print_str()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10080, debug=True)
