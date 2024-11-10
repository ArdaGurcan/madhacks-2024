import threading
import time
from enum import Enum, auto
import api
import logging

app = None
class Status(Enum):
    RUNNING = auto()
    WAITING = auto()
    ZOMBIE = auto()

INTERVAL = 60 * 0.2
time_value = -1
users = dict()

timer_status = Status.ZOMBIE
timer_value_lock = threading.Lock()
timer_status_lock = threading.Lock()

def timer():
    global timer_status
    global time_value
    global users

    while True:
        time.sleep(1)
        with timer_value_lock:
            with timer_status_lock:
                time_value -= 1

                if timer_status == Status.WAITING:
                    if not users:
                        api.live_session = False
                        return

                    users.clear()
                    app.logger.info("Users have been cleared")

                    time_value = INTERVAL
                    timer_status = Status.RUNNING
        time.sleep(10)

def start_timer():
    global timer_status
    global time_value

    time_value = INTERVAL
    clock_thread = threading.Thread(target=timer, daemon=True)
    clock_thread.start()

def wait_timer(a):
    global timer_status
    global app
    app = a
    with timer_value_lock:
        with timer_status_lock:
            timer_status = Status.WAITING

def session_init():
    global users

    users.clear()
    start_timer()

def update_user_runtime(username, runtime):
    global users
    if username in users:
        users[username] = runtime if runtime < users[username] else users[username]
    else:
        users[username] = runtime
