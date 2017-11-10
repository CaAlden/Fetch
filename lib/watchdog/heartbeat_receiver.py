import socket
import time

import watchdog

PROG_START = time.time()

def dummy():
    print("in dummy...")
    time.sleep(10)
    print("end of dummy...")

def on_success(hb):
    print("[HEARTBEAT] - " + hb['msg'] + " " + str(time.time() - PROG_START))

def on_err(e):
    print("[ERROR] {}!".format(e))

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', 0))
    sock.settimeout(0.5)

    # Get port we bound to
    print("[bound] {}".format(sock.getsockname()[1]))
    time.sleep(6)
    print("[watchdog] - starting")
    watchdog.heartbeat_watchdog(dummy, sock, 1, on_success, on_err)

if __name__ == '__main__':
    main()
