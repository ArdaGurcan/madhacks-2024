import sys
import random

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 gen.py <file>")
    result = ""
    with open(sys.argv[1], "r") as f:
        for line in f:
            if line.split(" ")[0] in ["Input:", "Output:", "Explanation:"]:
                result += "> "
            result += line
            if line == "":
                result += "\n"
            result += "\n"
    with open("6.json", "w") as f:
        f.write(result)
