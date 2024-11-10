from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
import logging

import urllib.parse
import json
import base64

import check_code
import session

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

live_session = False

@app.route("/")
@cross_origin()
def main():
    return "working"

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

    if encoded_username:
        username = decode(encoded_username)
        if data["result"]: # If all tests have passed
            session.update_user_runtime(username, data["runtime"])

    # Call the function to check the decoded code
    return json.dumps(data), 200

@app.route('/problem', methods=['GET', 'POST'])
@cross_origin()
def problem():
    q_id = request.args.get('q_id')
    with open("problems/" + str(q_id) + ".json", "r") as file:
        return json.dumps(json.load(file)), 200

@app.route('/leaderboard', methods=['GET', 'POST'])
@cross_origin()
def leaderboard():
    lb = [[username, time] for username, time in session.users.items()]
    lb.sort(key=lambda x: x[1])
    return json.dumps(lb), 200

@app.route('/session', methods=['GET', 'POST'])
@cross_origin()
def session_start():
    global live_session

    if not live_session:
        live_session = True
        session.session_init()

    app.logger.info("session")
    app.logger.info(json.dumps({"timer": session.time_value}))
    return json.dumps({"timer": session.time_value})

@app.route('/check_alive', methods=['GET', 'POST'])
@cross_origin()
def alive():
    session.wait_timer()
    ret = json.dumps({"timer": session.time_value, "users": list(session.users.keys())})
    app.logger.info("/check_alive")
    app.logger.info(ret)
    return ret
