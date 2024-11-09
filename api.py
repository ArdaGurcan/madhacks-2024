from flask import Flask
from flask import request

import json
import base64

import check_code

app = Flask(__name__)

@app.route("/")
def check():
    return "working"

def decode(encoded_code):
    # Convert the encoded code from a string to bytes, decode it, and return as a string
    return base64.urlsafe_b64decode(encoded_code.encode()).decode()

@app.route('/check', methods=['GET', 'POST'])
def login():
    q_id = request.args.get('q_id')
    encoded_function_name = request.args.get('f_name')
    encoded_code = request.args.get('code')
    
    # Decode the received code
    code = decode(encoded_code)
    function_name = decode(encoded_function_name)
    
    # Call the function to check the decoded code
    return json.dumps(check_code.check(q_id, code, function_name)), 200
