import tempfile
import importlib.util
import subprocess
import time
import json

def check(q_id, code, func_name):
    file_ext = 'py'
    with open("problems/id.txt", "r") as f:
        assert q_id in list(map(lambda x: int(x.strip()), f.readlines()))

    p_data = None
    problem_path = "problems/" + str(q_id) + ".json"
    with open(problem_path, "r") as file:
        p_data = json.load(file)

    assert p_data != None

    code_f = tempfile.NamedTemporaryFile(suffix=".py")
    code_f.write(code.encode())
    code_f.seek(0)

    spec = importlib.util.spec_from_file_location(func_name, temp_file_path)
    temp_module = importlib.util.module_from_spec(spec)
    sys.modules[func_name] = temp_module
    spec.loader.exec_module(temp_module)

    result = eval("temp_module.my_temp_function(" + p_data["args"] + ")")
    # for i in range(p_data["n"]): # Run tests
        # start_time = time.perf_counter()
    # result = eval(func_name + "(" + p_data ")")
        # runtime = time.perf_counter() - start_time
        # output = result.stdout.strip()

    # return {"result": "pass", "time": 0.123}

if __name__ == '__main__':
    check(0, "print(\"Hello World\")")
