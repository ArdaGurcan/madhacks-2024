from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit
import logging
import urllib.parse
import json
import base64

import check_code
import session
import threading
import random
import time

app = Flask(__name__)
CORS(app)

# Initialize SocketIO with async_mode set to 'eventlet'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

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
        app.logger.info("Restarting Session")
        live_session = True
        session.session_init()

    app.logger.info("session")
    return json.dumps({"timer": session.time_value})

@app.route('/check_alive', methods=['GET', 'POST'])
@cross_origin()
def alive():
    ret = json.dumps({"timer": session.time_value, "users": list(session.users.keys())})
    session.wait_timer(app)
    app.logger.info("/check_alive")
    app.logger.info(f"users: {session.alive_users}")
    session.users_sent = True
    return ret

# WebSocket Events
@socketio.on('connect')
def handle_connect():
    app.logger.info('Client connected')
    #emit('message', {'message': 'Welcome to the WebSocket server!'})
    #time.sleep(random.randrange(1,int(session.INTERVAL) - 5))  # Wait for 1 to 5 seconds
    message = {
        'message': 'Hello from server!',
        'value': random.choice(["squid", "lightning", "bomb"])
    }
    #emit('message', message)

@socketio.on('disconnect')
def handle_disconnect():
    app.logger.info('Client removed')

# Handle message from frontend
@socketio.on('frontend_message')
def handle_frontend_message(data):
    app.logger.info('Received message from frontend: %s', data)
    # Emit the received message back to the frontend
    message = {
        'username': data['username'],
        'action': data['action'],

    }
    socketio.emit('message',  message)

@socketio.on('new_user')
def handle_new_user(data):
    app.logger.info(f"User successfully added: {data['username']}")
    session.alive_users.add(data['username'])

@socketio.on('kill_user')
def handle_new_user(data):
    app.logger.info(f"User successfully removed: {data['username']}")
    session.alive_users.remove(data['username'])

if __name__ == '__main__':
    # Start the background thread for sending messages
    # socketio.start_background_task(target=background_thread)
    # Run the Flask app with SocketIO using eventlet
    socketio.run(app, host='0.0.0.0', port=6789, debug=True)
