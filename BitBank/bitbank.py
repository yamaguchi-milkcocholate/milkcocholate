from flask import Flask, jsonify, request
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/API')
from API.BitBankPubAPIManager import BitBankPubAPIManager
import json


app = Flask(__name__)
bitBankPubAPIManager = BitBankPubAPIManager()


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


@app.route('/public/<pair>', methods=['GET'])
def api_public_ticker(pair):
    if not pair:
        pair = 'btc_jpy'
    value = bitBankPubAPIManager.get_ticker(pair)
    return jsonify(value)


@app.route('/public/<pair>', methods=['GET'])
def api_public_depth(pair):
    if not pair:
        pair = 'btc_jpy'
    value = bitBankPubAPIManager.get_depth(pair)
    return jsonify(value)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10080, debug=True)
