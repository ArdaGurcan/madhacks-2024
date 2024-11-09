import tempfile
import importlib.util
import subprocess
import time
import json
import sys
import ast

def check(q_id, code, func_name):
    print(f"q_id: {q_id}, code: {code}, func_name: {func_name}")
    total_runtime = []
    file_ext = 'py'
    errcode = None

    with open("problems/id.txt", "r") as f:
        assert q_id in list(map(lambda x: x.strip(), f.readlines()))

    p_data = None
    problem_path = "problems/" + str(q_id) + ".json"
    with open(problem_path, "r") as file:
        p_data = json.load(file)

    assert p_data != None

    code_f = tempfile.NamedTemporaryFile(suffix=".py")
    code_f.write(code.encode())
    code_f.seek(0)

    try:
        spec = importlib.util.spec_from_file_location("usercode", code_f.name)
        usercode = importlib.util.module_from_spec(spec)
        sys.modules["usercode"] = usercode
        spec.loader.exec_module(usercode)

        for i in range(p_data["n"]): # Run tests
            start_time = time.perf_counter()

            try:
                result = ast.literal_eval("usercode." + func_name + "(" + p_data["testcase_" + str(i) + "_args"] + ")")
            except Exception as e:
                errcode = e

            runtime = time.perf_counter() - start_time

            if (result != ast.literal_eval(p_data["testcase_" + str(i) + "sol"])):
                # print({"result": False, "error": errcode, "runtime": sum(total_runtime), "n": i})
                return {"result": False, "error": errcode, "runtime": sum(total_runtime), "n": i}
    except Exception as e:
        errcode = e
        return {"result": True, "error": errcode, "runtime": sum(total_runtime), "n": 0}

    # print({"result": True, "error": errcode, "runtime": sum(total_runtime), "n": p_data["n"]})
    return {"result": True, "error": errcode, "runtime": sum(total_runtime), "n": p_data["n"]}

if __name__ == '__main__':
    function_code = """
def my_temp_function(x, y):
    return y *
"""
    print(check(1, function_code, "my_temp_function"))
