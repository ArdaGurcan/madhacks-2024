import tempfile
import importlib.util
import subprocess
import time
import json
import sys
import ast

def check(q_id, code, func_name, app):
    # print(f"q_id: {q_id}, code: {code}, func_name: {func_name}")
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
    code_f.write(b"from typing import *\n")
    code_f.write(code.encode())
    code_f.seek(0)

    try:
        spec = importlib.util.spec_from_file_location("usercode", code_f.name)
        usercode = importlib.util.module_from_spec(spec)
        sys.modules["usercode"] = usercode
        spec.loader.exec_module(usercode)

        for i in range(p_data["n"]): # Run tests
            start_time = time.perf_counter()
            app.logger.info("usercode." + func_name + "(" + p_data["testcase_" + str(i) + "_args"] + ")")
            result = eval("usercode." + func_name + "(" + p_data["testcase_" + str(i) + "_args"] + ")")

            if result != p_data["testcase_" + str(i) + "_sol"]:
                raise AssertionError(f"For testcase {i}, expected {p_data['testcase_' + str(i) + '_sol']}, got {result}")

            runtime = time.perf_counter() - start_time
            total_runtime.append(runtime)
    except Exception as e:
        errcode = e
        return {"result": False, "error": str(errcode), "runtime": sum(total_runtime), "n": len(total_runtime)}

    return {"result": True, "error": str(errcode), "runtime": sum(total_runtime), "n": p_data["n"]}

if __name__ == '__main__':
    function_code = """
def twoSum(nums: List[int], target: int) -> List[int]:
  for i, x in enumerate(nums):
    for j in range(i + 1, len(nums)):
        if x + nums[j] == target:
            return [i, j]
  return None
"""
    """
import re
def isPalindrome(s: str) -> bool:
    s = re.sub(r'\W+', '', s).lower()
    return s[::-1] == s
    """
    print(check("1", function_code, "twoSum"))
