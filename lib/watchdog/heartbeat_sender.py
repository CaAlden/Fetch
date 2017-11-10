import argparse
import json
import logging
import sys
import socket
import time

def get_args():
    parser = argparse.ArgumentParser("Simple client for sending heartbeats to the given host:port")
    parser.add_argument('host', type=str, help="host to send heartbeats to.")
    parser.add_argument('--port', type=int, help="port on the host where watchdog is running")
    parser.add_argument('--freq', type=float, help="Frequency in seconds to send heartbeat", default=0.250)
    args = parser.parse_args()

    if ':' in args.host:
        if args.port is not None:
            sys.stderr.write('Either specify a port or use <host>:<port> format; not both.\n')
            sys.stderr.flush()
            sys.exit(-1)
        else:
            host_port = args.host.split(':')
            try:
                host = host_port[0]
                port = int(host_port[1])
                return (host, port), args.freq
            except:
                sys.stderr.write('Error parsing args: {}\n'.format(parser.host))
                sys.stderr.flush()
                sys.exit(-1)
    else:
        return (args.host, args.port), args.freq

def send_heartbeat(sock):
    msg = json.dumps({'type': 'heartbeat', 'msg': 'From {}'.format(__file__), 'ts': time.time()})
    try:
        sock.send(msg.encode('utf-8'))
    except ConnectionRefusedError:
        logging.warn("Connection refused")
        return
    except Exception as e:
        logging.error("Got: {}".format(e))
        raise e

def main():
    addr, freq = get_args()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(addr)
    while True:
        time.sleep(freq)
        send_heartbeat(sock)

if __name__ == '__main__':
    main()
