from typing import Any, AnyStr, BinaryIO, IO, Text, TextIO, Iterable, Iterator, List, Optional, Type, Tuple, TypeVar, Union
from mmap import mmap
from types import TracebackType

_bytearray_like = Union[bytearray, mmap]

DEFAULT_BUFFER_SIZE = ...  # type: int

class BlockingIOError(IOError):
    characters_written = ...  # type: int

class UnsupportedOperation(ValueError, IOError): ...

_T = TypeVar("_T")

class _IOBase(BinaryIO):
    @property
    def closed(self) -> bool: ...
    def _checkClosed(self) -> None: ...
    def _checkReadable(self) -> None: ...
    def _checkSeekable(self) -> None: ...
    def _checkWritable(self) -> None: ...
    # All these methods are concrete here (you can instantiate this)
    def close(self) -> None: ...
    def fileno(self) -> int: ...
    def flush(self) -> None: ...
    def isatty(self) -> bool: ...
    def readable(self) -> bool: ...
    def seek(self, offset: int, whence: int = ...) -> int: ...
    def seekable(self) -> bool: ...
    def tell(self) -> int: ...
    def truncate(self, size: Optional[int] = ...) -> int: ...
    def writable(self) -> bool: ...
    def __enter__(self: _T) -> _T: ...
    def __exit__(self, t: Optional[Type[BaseException]], value: Optional[BaseException], traceback: Optional[Any]) -> bool: ...
    def __iter__(self: _T) -> _T: ...
    # The parameter type of writelines[s]() is determined by that of write():
    def writelines(self, lines: Iterable[bytes]) -> None: ...
    # The return type of readline[s]() and next() is determined by that of read():
    def readline(self, limit: int = ...) -> bytes: ...
    def readlines(self, hint: int = ...) -> list[bytes]: ...
    def next(self) -> bytes: ...

class _BufferedIOBase(_IOBase):
    def read1(self, n: int) -> bytes: ...
    def read(self, size: int = ...) -> bytes: ...
    def readinto(self, buffer: _bytearray_like) -> int: ...
    def write(self, s: bytes) -> int: ...
    def detach(self) -> _IOBase: ...

class BufferedRWPair(_BufferedIOBase):
    def __init__(self, reader: _RawIOBase, writer: _RawIOBase,
                 buffer_size: int = ..., max_buffer_size: int = ...) -> None: ...
    def peek(self, n: int = ...) -> bytes: ...
    def __enter__(self) -> BufferedRWPair: ...

class BufferedRandom(_BufferedIOBase):
    mode = ...  # type: str
    name = ...  # type: str
    raw = ...  # type: _IOBase
    def __init__(self, raw: _IOBase,
                 buffer_size: int = ...,
                 max_buffer_size: int = ...) -> None: ...
    def peek(self, n: int = ...) -> bytes: ...

class BufferedReader(_BufferedIOBase):
    mode = ...  # type: str
    name = ...  # type: str
    raw = ...  # type: _IOBase
    def __init__(self, raw: _IOBase, buffer_size: int = ...) -> None: ...
    def peek(self, n: int = ...) -> bytes: ...

class BufferedWriter(_BufferedIOBase):
    name = ...  # type: str
    raw = ...  # type: _IOBase
    mode = ...  # type: str
    def __init__(self, raw: _IOBase,
                 buffer_size: int = ...,
                 max_buffer_size: int = ...) -> None: ...

class BytesIO(_BufferedIOBase):
    def __init__(self, initial_bytes: bytes = ...) -> None: ...
    def __setstate__(self, tuple) -> None: ...
    def __getstate__(self) -> tuple: ...
    def getvalue(self) -> bytes: ...
    def write(self, s: bytes) -> int: ...
    def writelines(self, lines: Iterable[bytes]) -> None: ...
    def read1(self, size: int) -> bytes: ...
    def next(self) -> bytes: ...

class _RawIOBase(_IOBase):
    def readall(self) -> str: ...
    def read(self, n: int = ...) -> str: ...

class FileIO(_RawIOBase, BytesIO):  # type: ignore  # for __enter__
    mode = ...  # type: str
    closefd = ...  # type: bool
    def __init__(self, file: Union[str, int], mode: str = ..., closefd: bool = ...) -> None: ...
    def readinto(self, buffer: _bytearray_like)-> int: ...
    def write(self, pbuf: str) -> int: ...

class IncrementalNewlineDecoder(object):
    newlines = ...  # type: Union[str, unicode]
    def __init__(self, decoder, translate, z=...) -> None: ...
    def decode(self, input, final) -> Any: ...
    def getstate(self) -> Tuple[Any, int]: ...
    def setstate(self, state: Tuple[Any, int]) -> None: ...
    def reset(self) -> None: ...


# Note: In the actual _io.py, _TextIOBase inherits from _IOBase.
class _TextIOBase(TextIO):
    errors = ...  # type: Optional[str]
    # TODO: On _TextIOBase, this is always None. But it's unicode/bytes in subclasses.
    newlines = ...  # type: Union[None, unicode, bytes]
    encoding = ...  # type: str
    @property
    def closed(self) -> bool: ...
    def _checkClosed(self) -> None: ...
    def _checkReadable(self) -> None: ...
    def _checkSeekable(self) -> None: ...
    def _checkWritable(self) -> None: ...
    def close(self) -> None: ...
    def detach(self) -> IO: ...
    def fileno(self) -> int: ...
    def flush(self) -> None: ...
    def isatty(self) -> bool: ...
    def next(self) -> unicode: ...
    def read(self, size: int = ...) -> unicode: ...
    def readable(self) -> bool: ...
    def readline(self, limit: int = ...) -> unicode: ...
    def readlines(self, hint: int = ...) -> list[unicode]: ...
    def seek(self, offset: int, whence: int = ...) -> int: ...
    def seekable(self) -> bool: ...
    def tell(self) -> int: ...
    def truncate(self, size: Optional[int] = ...) -> int: ...
    def writable(self) -> bool: ...
    def write(self, pbuf: unicode) -> int: ...
    def writelines(self, lines: Iterable[unicode]) -> None: ...
    def __enter__(self: _T) -> _T: ...
    def __exit__(self, t: Optional[Type[BaseException]], value: Optional[BaseException], traceback: Optional[Any]) -> bool: ...
    def __iter__(self: _T) -> _T: ...

class StringIO(_TextIOBase):
    line_buffering = ...  # type: bool
    def __init__(self,
                 initial_value: Optional[unicode] = ...,
                 newline: Optional[unicode] = ...) -> None: ...
    def __setstate__(self, state: tuple) -> None: ...
    def __getstate__(self) -> tuple: ...
    def getvalue(self) -> unicode: ...

class TextIOWrapper(_TextIOBase):
    name = ...  # type: str
    line_buffering = ...  # type: bool
    buffer = ...  # type: BinaryIO
    _CHUNK_SIZE = ...  # type: int
    def __init__(self, buffer: IO,
                 encoding: Optional[Text] = ...,
                 errors: Optional[Text] = ...,
                 newline: Optional[Text] = ...,
                 line_buffering: bool = ...,
                 write_through: bool = ...) -> None: ...

def open(file: Union[str, unicode, int],
         mode: unicode = ...,
         buffering: int = ...,
         encoding: Optional[Text] = ...,
         errors: Optional[Text] = ...,
         newline: Optional[Text] = ...,
         closefd: bool = ...) -> IO[Any]: ...
