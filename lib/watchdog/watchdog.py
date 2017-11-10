import logging
import json
import os
from time import time

from multiprocessing import Process
from signal import SIGKILL

def default_timeout_handler(process):
    os.kill(process.pid, SIGKILL)

def heartbeat_watchdog(run, hb_conn, timeout, on_success, on_err, on_timeout=default_timeout_handler):
    ''' Run the given function with a heartbeat watchdog'''
    logging.info("Watchdog running, executing watched function")
    subproc = Process(target=run)
    subproc.start()
    last = time()
    while subproc.is_alive():
        hb = get_heartbeat(hb_conn, on_success, on_err)
        if hb is None:
            if time() - last > timeout:
                on_timeout(subproc)
                return
        else:
            logging.info("Got a heartbeat...")
            last = hb['ts']

def get_heartbeat(connection, success, err):
    """Get heartbeats on the connection, if one is available.
       Args:
           connection - A connection to receive on. (assumed to be a Stream)
           success    - Function to call when the heartbeat is received.
           err        - Function to call when timeout is reached without a heartbeat."""
    try:
        hb = json.loads(connection.recv(100).decode('utf-8'))
        success(hb)
        return hb
    except Exception as e:
        err(e)
        return None
