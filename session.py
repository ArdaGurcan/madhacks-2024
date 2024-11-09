import threading
import time

INTERVAL = 60 * 10
time_value = -1
users = dict()
kill_timer = 0
clock_thread = None

def timer():
    time.sleep(1)
    time_value -= 1

    if kill_timer:
        return

def start_timer():
    time_value = INTERVAL
    clock_thread = threading.Thread(target=timer, daemon=True)
    clock_thread.start()

def kill_timer():
    kill_timer = 1

    if clock_thread:
        clock_thread.join()

def session_init():
    users = dict()
    start_timer()

def update_user_runtime(username, runtime):
    if username in users:
        users[username] = runtime if runtime < users[username] else users[username]
    else:
        users[username] = runtime
