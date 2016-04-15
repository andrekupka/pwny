import itertools
import socket
import telnetlib
import time
from functools import wraps
from .binarystore import BinaryStore
from .ropchain import RopChain
from .util import encode_arg


def delayed(f):
    """
    Decorates an instance method of a class and delays its execution by the
    value of the instances internal _delay field.
    """
    @wraps(f)
    def _inner(self, *args, **kwargs):
        time.sleep(self._delay)
        return f(self, *args, **kwargs)
    return _inner


class Pwny:
    def __init__(self, sock=None, dump_received=True, try_decode_received=True,
                 word_size=8, little_endian=True, delay=0.1,
                 confirm_send=False, binaries=None):
        """
        Constructor.

        :param socket.socket sock: a initialized non-connected socket or None if a socket
            shall be created
        """
        self._sock = sock or socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._dump_received = dump_received
        self._try_decode_received = try_decode_received
        self._word_size = word_size
        self._little_endian = little_endian
        self._delay = delay
        self._confirm_send = confirm_send
        self._binary_store = BinaryStore()
        binaries = binaries or list()
        for binary in binaries:
            self._binary_store.add_binary(binary)

    def connect(self, host, port):
        """
        Connects to the given host and port.
        """
        self._sock.connect((host, port))

    def half_close(self):
        """
        Half closes the internal socket so that a remote read will fail but
        remote messages can still be received.
        """
        self._sock.shutdown(socket.SHUT_WR)

    def close(self):
        """
        Closes the internal socket.
        """
        self._sock.close()

    def get_socket(self):
        """
        Returns the internal socket.
        """
        return self._sock

    def set_little_endian(self, little_endian):
        """
        Sets if the exploit assumes a little or big endian system.
        """
        self._little_endian = little_endian

    def set_word_size(self, word_size):
        """Sets the word size of the exploited binary.

        :param int word_wize: must be 1, 2, 4 or 8
        """
        if word_size not in [1,2,4,8]:
            raise Exception("Illegal word size: %d".format(word_size))
        self._word_size = word_size

    def set_dump_received(self, dump_received):
        """
        Sets whether received data should be dumped to stdout.
        """
        self._dump_received = dump_received

    def set_try_decode_received(self, try_decode_received):
        """
        Sets whether received binary data should be tried to be decoded.
        """
        self._try_decode_received = try_decode_received

    def set_confirm_send(self, confirm_send):
        """
        Sets whether the user must confirm sending data by pressing enter.
        """
        self._confirm_send = confirm_send

    def set_delay(self, delay):
        """
        Sets the delay between single send and/or received operations.

        :param delay: the delay in seconds
        :type delay: float
        """
        self._delay = delay

    def add_binary(self, binary, bin_name=None):
        """
        Adds a binary to the internal binary store, that can be used to resolve
        symbols to addresses.

        :param binary: the binary that is to be added
        :type binary: BinaryBase and its subclasses
        :param bin_name: the name of the binary, if None the binaries internal
            name is used
        :type bin_name: str or None
        """
        self._binary_store.add_binary(binary, bin_name)

    @delayed
    @encode_arg(0)
    def send(self, data):
        """
        Tries to encode the given data as bytes and send it to the remote.

        :param data: the data that is send to the remote
        :type data: bytes or str
        """
        if self._confirm_send:
            self.prompt("Press enter to send:\n{}".format(data))
        self._sock.sendall(data)

    @delayed
    def recv(self, buffer_size=4096):
        """
        Receives data from the remote.

        :param buffer_size: the size of the receive buffer and thus the maximum
            amount of data that is received at once
        :type buffer_size: int
        """
        received = self._sock.recv(buffer_size)
        self._try_decode_and_print(received)
        return received

    @delayed
    def recv_length(self, length):
        """
        Receives the given amount of bytes from the remote.

        :param length: the length that should be received in bytes
        :type length: int
        """
        received = b""
        while len(received) < length:
            received += self._sock.recv(length - len(received))
        self._try_decode_and_print(received)
        return received

    @delayed
    @encode_arg(0)
    def recv_expect(self, expected):
        """
        Receives the expected string from the remote.

        :param expected: the string that is expected to be received from the
            remote
        :type expected: bytes or str
        """
        received = b""
        while received != expected:
            received += self._sock.recv(1)
        self._try_decode_and_print(received)
        return received

    @delayed
    @encode_arg(0)
    def recv_until(self, until):
        """
        Receives until the received data contains the given string.

        :param until: the string that is expected to be received eventually
            from the remote
        :type until: bytes or str
        """
        received = b""
        while until not in received:
            received += self._sock.recv(1)
        self._try_decode_and_print(received)
        return received

    def recv_line(self):
        """
        Receives from the remote until a newline is received.
        """
        return self.recv_until(b"\n")

    def recv_lines(self, count):
        for _ in range(count):
            self.recv_line(self)

    def prompt(self, prompt=None):
        """
        Prompts the user for some input.

        :param prompt: the prompt that is displayed to the user
        :type prompt: str
        """
        prompt = prompt or ""
        return input(prompt)

    def interact(self):
        """
        Lets the user interactively communicate with the remote.
        """
        t = telnetlib.Telnet()
        t.sock = self._sock
        t.interact()

    def _try_decode_and_print(self, data):
        """
        Prints the given data to stdout if self._dump_received is True. If
        self._try_decode_received is True, the given data will be tried to be
        decoded. If this does not work the raw data will be printed.
        """
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
        """
        Creates a new rop chain.
        """
        return RopChain(self)

    @staticmethod
    def from_socket(sock):
        """
        Creates a new Pwny that wraps the given socket.

        :param sock: that socket that is to be wrapped
        :type sock: socket.socket
        """
        return Pwny(sock)
