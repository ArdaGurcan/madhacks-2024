from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin

import urllib.parse
import json
import base64

import check_code

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
users = dict()

@app.route("/")
@cross_origin()
def main():
    return "working"

def update_user_runtime(username, runtime):
    if username in users:
        users[username] = runtime if runtime < users[username] else users[username]
    else:
        users[username] = runtime

def decode(encoded_data):
    # Convert the encoded code from a string to bytes, decode it, and return as a string
    return urllib.parse.unquote(encoded_data)

@app.route('/check', methods=['GET', 'POST'])
@cross_origin()
def check():
    q_id = request.args.get('q_id')
    encoded_function_name = request.args.get('f_name')
    encoded_code = request.args.get('code')
    encoded_username = request.args.get('username')

    # Decode the received code
    code = decode(encoded_code)
    function_name = decode(encoded_function_name)

    data = check_code.check(q_id, code, function_name)

    if username:
        username = decode(encoded_username)
        if data["result"]: # If all tests have passed
            update_user_runtime(username, data["runtime"])

    # Call the function to check the decoded code
    return json.dumps(data), 200

@app.route('/problem', methods=['GET', 'POST'])
@cross_origin()
def problem():
    q_id = request.args.get('q_id')
    with open("problems/" + str(q_id) + ".json", "r") as file:
        return json.dumps(json.load(file)), 200

