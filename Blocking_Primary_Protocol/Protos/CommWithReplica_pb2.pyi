from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Address(_message.Message):
    __slots__ = ["ip", "name", "port"]
    IP_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    ip: str
    name: str
    port: int
    def __init__(self, name: _Optional[str] = ..., ip: _Optional[str] = ..., port: _Optional[int] = ...) -> None: ...

class ConnectToPRRequest(_message.Message):
    __slots__ = ["replica", "request"]
    REPLICA_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    replica: Address
    request: WriteRequest
    def __init__(self, request: _Optional[_Union[WriteRequest, _Mapping]] = ..., replica: _Optional[_Union[Address, _Mapping]] = ...) -> None: ...

class DeleteRequest(_message.Message):
    __slots__ = ["uuid"]
    UUID_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    def __init__(self, uuid: _Optional[str] = ...) -> None: ...

class ReadRequest(_message.Message):
    __slots__ = ["uuid"]
    UUID_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    def __init__(self, uuid: _Optional[str] = ...) -> None: ...

class ReadResponse(_message.Message):
    __slots__ = ["content", "name", "status", "version"]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    content: str
    name: str
    status: str
    version: _timestamp_pb2.Timestamp
    def __init__(self, status: _Optional[str] = ..., name: _Optional[str] = ..., content: _Optional[str] = ..., version: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class StatusRepReq(_message.Message):
    __slots__ = ["status"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: str
    def __init__(self, status: _Optional[str] = ...) -> None: ...

class WriteRequest(_message.Message):
    __slots__ = ["content", "name", "uuid"]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    content: str
    name: str
    uuid: str
    def __init__(self, uuid: _Optional[str] = ..., name: _Optional[str] = ..., content: _Optional[str] = ...) -> None: ...
