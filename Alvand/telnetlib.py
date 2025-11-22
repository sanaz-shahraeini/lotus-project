import socket
import time
from typing import Optional


class Telnet:
    """Minimal Telnet-like client used by the project.

    This is *not* a full replacement for the old stdlib telnetlib, but it
    supports the subset of behavior used in Alvand.utils.PanasonicNS500:

    - constructor(host, port=23, timeout=10)
    - read_until(expected: bytes, timeout: Optional[float] = None) -> bytes
    - write(data: bytes) -> None
    - read_very_eager() -> bytes
    - close() -> None
    """

    def __init__(self, host: str, port: int = 23, timeout: float = 10.0):
        self._sock = socket.create_connection((host, port), timeout=timeout)
        # Default timeout for subsequent operations
        self._sock.settimeout(timeout)

    # API compatible with stdlib telnetlib.Telnet.read_until
    def read_until(self, expected: bytes, timeout: Optional[float] = None) -> bytes:
        if not isinstance(expected, (bytes, bytearray)):
            raise TypeError("expected must be bytes")

        # Use a simple loop with deadline to accumulate data
        buf = bytearray()
        end_time = None
        if timeout is not None:
            end_time = time.time() + timeout

        while True:
            if expected in buf:
                break

            if end_time is not None and time.time() >= end_time:
                break

            try:
                chunk = self._sock.recv(1024)
            except socket.timeout:
                break

            if not chunk:
                # Remote closed or no more data
                break

            buf.extend(chunk)

        return bytes(buf)

    def write(self, data: bytes) -> None:
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("data must be bytes")
        self._sock.sendall(data)

    def read_very_eager(self) -> bytes:
        """Non-blocking read of whatever data is already available."""
        self._sock.setblocking(False)
        chunks = []
        try:
            while True:
                try:
                    chunk = self._sock.recv(4096)
                except BlockingIOError:
                    break
                if not chunk:
                    break
                chunks.append(chunk)
        finally:
            self._sock.setblocking(True)
        return b"".join(chunks)

    def close(self) -> None:
        try:
            self._sock.close()
        except OSError:
            pass
