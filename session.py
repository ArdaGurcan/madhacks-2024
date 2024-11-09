import threading
import time
from enum import Enum, auto

class Status(Enum):
    RUNNING = auto()
    WAITING = auto()
    ZOMBIE = auto()

INTERVAL = 60 * 10
time_value = -1
users = dict()

timer_status = Status.ZOMBIE

def timer():
    time.sleep(1)
    time_value -= 1
    if time_value <= 0:
        timer_status == Status.ZOMBIE

    if timer_status == Status.WAITING:
        time.sleep(30)
        timer_status = Status.RUNNING
        time_value = INTERVAL

    if timer_status == Status.ZOMBIE:
        return

def start_timer():
    if timer_status == Status.ZOMBIE:
        time_value = INTERVAL
        clock_thread = threading.Thread(target=timer, daemon=True)
        clock_thread.start()

def wait_timer():
    timer_status = Status.WAITING

def session_init():
    users = dict()
    start_timer()

def update_user_runtime(username, runtime):
    if username in users:
        users[username] = runtime if runtime < users[username] else users[username]
    else:
        users[username] = runtime
