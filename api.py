from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin

import json
import base64

import check_code

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
@cross_origin()
def check():
    return "working"

def decode(encoded_code):
    # Convert the encoded code from a string to bytes, decode it, and return as a string
    return base64.urlsafe_b64decode(encoded_code.encode()).decode()

@app.route('/check', methods=['GET', 'POST'])
@cross_origin()
def login():
    q_id = request.args.get('q_id')
    encoded_function_name = request.args.get('f_name')
    encoded_code = request.args.get('code')
    
    # Decode the received code
    code = decode(encoded_code)
    function_name = decode(encoded_function_name)
    
    # Call the function to check the decoded code
    return json.dumps(check_code.check(q_id, code, function_name)), 200
