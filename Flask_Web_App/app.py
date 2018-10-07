# coding:utf-8
from flask import Flask, jsonify, request, render_template
app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():
    prefectures = list()
    prefectures.append(('北海度', 1))
    prefectures.append(('aomori', 2))
    prefectures.append(('iwate', 3))
    prefectures.append(('miyagi', 4))
    prefectures.append(('akita', 5))
    prefectures.append(('yamagata', 6))
    prefectures.append(('fukusima', 7))
    prefectures.append(('ibaraki', 8))
    prefectures.append(('tochigi', 9))
    prefectures.append(('gunma', 10))
    prefectures.append(('chiba', 11))
    prefectures.append(('kanagawa', 12))
    return render_template('index.html', prefectures=prefectures)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
