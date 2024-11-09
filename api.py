from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/")
def check():
    return "working"

@app.route('/login', methods=['GET', 'POST'])
def login():
    q_id = request.args.get('q_id')
    code = request.args.get('code')
    # call the function to check the code
