import itertools
import socket
import telnetlib
import time
from functools import wraps
from .ropchain import RopChain
from .util import encode_arg


def delayed(f):
    @wraps(f)
    def _inner(self, *args, **kwargs):
        time.sleep(self._delay)
        return f(self, *args, **kwargs)
    return _inner


class Pwny:
    def __init__(self, sock=None):
        self._sock = sock or socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._dump_received = False
        self._try_decode_received = True
        self._delay = 0.1
        self._address_map = None
        self._little_endian = True
        self._word_size = 8

    def connect(self, host, port):
        self._sock.connect((host, port))

    def close(self):
        self._sock.close()

    def get_socket(self):
        return self._sock

    def set_little_endian(self, little_endian):
        self._little_endian = little_endian

    def set_word_size(self, word_size):
        if word_size not in [1,2,4,8]:
            raise Exception("Illegal word size: %d".format(word_size))
        self._word_size = word_size

    def set_dump_received(self, dump_received):
        self._dump_received = dump_received

    def set_try_decode_received(self, try_decode_received):
        self._try_decode_received = try_decode_received

    def set_delay(self, delay):
        self._delay = delay

    @delayed
    @encode_arg(0)
    def send(self, data):
        self._sock.sendall(data)

    @delayed
    def recv(self, buffer_size=4096):
        received = self._sock.recv(buffer_size)
        self._try_decode_and_print(received)
        return received

    @delayed
    def recv_length(self, length):
        received = b""
        while len(received) < length:
            received += self._sock.recv(length - len(received))
        self._try_decode_and_print(received)
        return received

    @delayed
    @encode_arg(0)
    def recv_expect(self, expected):
        received = b""
        while received != expected:
            received += self._sock.recv(1)
        self._try_decode_and_print(received)
        return received

    @delayed
    @encode_arg(0)
    def recv_until(self, until):
        received = b""
        while until not in received:
            received += self._sock.recv(1)
        self._try_decode_and_print(received)
        return received

    def recv_newline(self):
        return self.recv_until(b"\n")

    def prompt(self, prompt):
        return input(prompt)

    def interact(self):
        t = telnetlib.Telnet()
        t.sock = self._sock
        t.interact()

    def _try_decode_and_print(self, data):
        if not self._dump_received:
            return
        if self._try_decode_received:
            try:
                print(data.decode(), end="")
            except:
                print(data)
        else:
            print(data)

    def create_chain(self):
        return RopChain(self)

    @staticmethod
    def wrap_socket(sock):
        return Pwny(sock)
