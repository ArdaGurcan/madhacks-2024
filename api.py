from flask import Flask
from flask import request

import json

import check_code

app = Flask(__name__)

@app.route("/")
def check():
    return "working"

@app.route('/login', methods=['GET', 'POST'])
def login():
    q_id = request.args.get('q_id')
    code = request.args.get('code')
    # call the function to check the code
    return json.dumps(check_code.check(q_id, code)), 200
