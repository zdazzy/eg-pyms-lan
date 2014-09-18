#!/usr/bin/env python

__author__ = 'zdazzy'

import sys
from PyMS import PMSDevice


def print_usage_and_exit():
    print "Usage: ./pyms-socket.py <hostname> <password> [socket:state]..."
    print "   [socketN] - a pair X:Y where X - socket number (1-4), Y - state (0 - off, 1 - on)"
    sys.exit(1)

if __name__ != '__main__':
    raise Exception('This is a CLI script')

if len(sys.argv) < 4:
    print_usage_and_exit()

states = None

try:
    params = map(lambda p: map(int, p.split(':')), sys.argv[3:])
    states = dict((p[0] - 1, bool(p[1])) for p in params if p[0] in range(1, 5))
except ValueError:
    print_usage_and_exit()

if len(states) < 1:
    print_usage_and_exit()

dev = PMSDevice(sys.argv[1], sys.argv[2])
dev.set_socket_states(states)
