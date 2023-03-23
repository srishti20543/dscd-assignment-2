from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Address(_message.Message):
    __slots__ = ["IP", "name", "port"]
    IP: str
    IP_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    name: str
    port: int
    def __init__(self, name: _Optional[str] = ..., IP: _Optional[str] = ..., port: _Optional[int] = ...) -> None: ...

class SendDetailsOfPRResponse(_message.Message):
    __slots__ = ["Status"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    Status: str
    def __init__(self, Status: _Optional[str] = ...) -> None: ...
