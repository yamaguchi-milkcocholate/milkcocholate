from flask import Flask, jsonify, request
from API import bitbankpub


app = Flask(__name__)
bitBankPubAPIManager = bitbankpub.BitBankPubAPIManager()


@app.route("/", methods=['GET'])
def hello():
    return "BitBank 1.0"


@app.route('/public/ticker/<pair>', methods=['GET'])
def api_public_ticker(pair):
    if not pair:
        pair = 'btc_jpy'
    value = bitBankPubAPIManager.get_ticker(pair)
    return jsonify(value)


@app.route('/public/depth/<pair>', methods=['GET'])
def api_public_depth(pair):
    if not pair:
        pair = 'btc_jpy'
    value = bitBankPubAPIManager.get_depth(pair)
    return jsonify(value)


@app.route('/public/transactions/<pair>')
def api_public_transaction(pair):
    time = request.args.get('time')
    if not pair:
        pair = 'btc_jpy'
    value = bitBankPubAPIManager.get_transactions(pair, time)
    return jsonify(value)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10080, debug=True)
