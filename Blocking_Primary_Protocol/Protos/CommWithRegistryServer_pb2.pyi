from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Address(_message.Message):
    __slots__ = ["IP", "port"]
    IP: str
    IP_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    port: int
    def __init__(self, IP: _Optional[str] = ..., port: _Optional[int] = ...) -> None: ...

class RegisterReplicaResponse(_message.Message):
    __slots__ = ["primaryServerAddress", "status"]
    PRIMARYSERVERADDRESS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    primaryServerAddress: Address
    status: str
    def __init__(self, status: _Optional[str] = ..., primaryServerAddress: _Optional[_Union[Address, _Mapping]] = ...) -> None: ...

class ReplicaListResponse(_message.Message):
    __slots__ = ["name", "replicaServer"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    REPLICASERVER_FIELD_NUMBER: _ClassVar[int]
    name: str
    replicaServer: Address
    def __init__(self, name: _Optional[str] = ..., replicaServer: _Optional[_Union[Address, _Mapping]] = ...) -> None: ...
