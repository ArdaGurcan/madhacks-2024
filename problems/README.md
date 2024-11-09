# Format

Each problem is assigned a unique identifier. `id.txt` is a list of all existing identifiers.
Each problem will be specified in its own file by `problemid.json`. The fields of
the problems will be as follows
* `problem` *string*: The problem statement
* `n` *integer*: The number of testcases
* `testcase_i_args` *obj*: the arguments for the i'th testcase
* `testcase_i_sol` *obj*: the solution for the i'th testcase
