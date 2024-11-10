import threading
import time
from enum import Enum, auto
import api
import logging

app = None

INTERVAL = 60 * 0.5
time_value = -1
users = dict()
alive_users = set()
live_session = False

timer_status = 0
timer_value_lock = threading.Lock()
timer_status_lock = threading.Lock()

def timer():
    global timer_status
    global time_value
    global users
    global live_session

    while True:
        time.sleep(1)
        timer_value_lock.acquire()
        timer_status_lock.acquire()
        time_value -= 1

        app.logger.info(alive_users)

        if not alive_users:
            app.logger.info("Nobody is playing")
            live_session = False
            timer_value_lock.release()
            timer_status_lock.release()
            return

        if timer_status >= len(alive_users):
            users.clear()
            app.logger.info("Users have been cleared")

            time_value = INTERVAL
            timer_status = 0
            timer_value_lock.release()
            timer_status_lock.release()
            time.sleep(10)

        else:
            timer_value_lock.release()
            timer_status_lock.release()

def start_timer():
    global timer_status
    global time_value

    time_value = INTERVAL
    clock_thread = threading.Thread(target=timer, daemon=True)
    clock_thread.start()

def wait_timer():
    global timer_status
    global app
    with timer_value_lock:
        with timer_status_lock:
            timer_status += 1

def session_init(a):
    global live_session
    global app
    app = a
    # alive_users.clear()
    # users.clear()
    if not live_session:
        live_session = True
        start_timer()

def update_user_runtime(username, runtime):
    global users
    if username in users:
        users[username] = runtime if runtime < users[username] else users[username]
    else:
        users[username] = runtime
