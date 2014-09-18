__author__ = 'zdazzy'

import socket


class PMSDevice(object):
    """
    A reverse-engineered controller of the EG-PMS-LAN device socket states.

    The control over hardware socket schedule is not implemented.
    """

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    hostname = None
    password = None

    challenge = None
    socket_states = None

    def __init__(self, hostname, password):
        """
        Creates a device controller.

        TODO No password checking. Invalid password might yield unpredictable results.

        @type hostname: str
              Host name or address of the device.
        @type password: str
              Password to use to connect.
        @rtype: PMSDevice
        """
        self.hostname = hostname
        self.password = map(ord, (password + ' ' * 8)[:8])

    def set_socket_states(self, states):
        """
        Sets device sockets states.

        @type states: dict
              A dictionary {socket_number: socket_state}
                  socket_number : int 0 to 3
                  socket_state  : True/False to turn on/off correspondingly
        @rtype: None
        """
        self.__connect()
        self.__handshake()
        self.challenge = map(ord, self.__read_4_bytes())
        self.__send_bytes(self.__response(self.challenge))
        self.socket_states = self.__decode_socket_states(map(ord, self.__read_4_bytes()))
        new_states = [bool(states[t]) if t in states else None for t in range(0, 4)]
        self.__send_bytes(self.__encode_socket_states(new_states))
        self.__disconnect()

    def __connect(self):
        self.s.connect((self.hostname, 5000))

    def __disconnect(self):
        self.s.close()

    def __handshake(self):
        self.s.send('\x11')

    def __read_4_bytes(self):
        return self.s.recv(4)

    def __send_bytes(self, data):
        return self.s.send(''.join(map(chr, data)))

    def __response(self, challenge):
        part1 = (self.password[2] ^ challenge[0]) * self.password[0] ^ \
            (self.password[4] << 8 | self.password[6]) ^ \
            challenge[2]
        part2 = (self.password[3] ^ challenge[1]) * self.password[1] ^ \
            (self.password[5] << 8 | self.password[7]) ^ \
            challenge[3]

        return [
            part1 & 0xFF,
            part1 >> 8 & 0xFF,
            part2 & 0xFF,
            part2 >> 8 & 0xFF
        ]

    def __decode_socket_states(self, socket_states):
        # this could use some facelift
        states = [(self.challenge[2] ^ ((self.password[0] ^ (socket_states[t] - self.password[1])) - self.challenge[3])) & 0xFF
                  for t in range(0, 4)]

        for state in states:
            if not state in (0x11, 0x12, 0x21, 0x22):
                raise Exception('Invalid states')

        return [s >> 4 == 1 for s in states]

    def __encode_socket_states(self, new_states):
        new_states = [4 if s is None else 1 if s else 2 for s in new_states]
        # this is pretty ugly too
        return [((self.password[0] ^ (self.challenge[3] + (self.challenge[2] ^ new_states[3 - t]))) + self.password[1]) & 0xFF
                for t in range(0, 4)]
