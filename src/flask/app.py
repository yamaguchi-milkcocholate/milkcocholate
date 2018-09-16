from flask import Flask, render_template, request, redirect, url_for
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
     return "Hello Flask! aaa"

if __name__ == '__main__':
    app.debug = True  
    app.run(host='0.0.0.0')
