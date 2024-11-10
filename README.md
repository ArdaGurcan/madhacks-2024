# Create and run venv
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

# run flask app
```bash
flask --app api run
```

# check code
PUT or GET request to http://ardagurcan.com:5000/check
with parameters:
* code: the code to be checked (base64 encoded)
* q_id: the question id
* f_name: the function name (base64 encoded)

* test
