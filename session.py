import threading
import time
from enum import Enum, auto

class Status(Enum):
    RUNNING = auto()
    WAITING = auto()
    ZOMBIE = auto()

INTERVAL = 60 * 0.2
time_value = -1
users = dict()

timer_status = Status.ZOMBIE

def timer():
    global timer_status
    global time_value
    global users

    time.sleep(1)
    time_value -= 1
    if time_value <= 0:
        timer_status == Status.WAITING

    if timer_status == Status.WAITING:
        users.clear()
        timer_status = Status.RUNNING
        time_value = INTERVAL
        time.sleep(10)

def start_timer():
    global timer_status
    global time_value

    time_value = INTERVAL
    clock_thread = threading.Thread(target=timer, daemon=True)
    clock_thread.start()

def wait_timer():
    global timer_status
    timer_status = Status.WAITING

def session_init():
    global users

    users = dict()
    start_timer()

def update_user_runtime(username, runtime):
    global users
    if username in users:
        users[username] = runtime if runtime < users[username] else users[username]
    else:
        users[username] = runtime
