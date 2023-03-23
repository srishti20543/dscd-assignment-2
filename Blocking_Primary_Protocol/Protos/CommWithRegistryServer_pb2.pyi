import CommWithReplica_pb2 as _CommWithReplica_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RegisterReplicaResponse(_message.Message):
    __slots__ = ["primaryServerAddress", "selfName", "status"]
    PRIMARYSERVERADDRESS_FIELD_NUMBER: _ClassVar[int]
    SELFNAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    primaryServerAddress: _CommWithReplica_pb2.Address
    selfName: str
    status: str
    def __init__(self, status: _Optional[str] = ..., primaryServerAddress: _Optional[_Union[_CommWithReplica_pb2.Address, _Mapping]] = ..., selfName: _Optional[str] = ...) -> None: ...

class ReplicaListResponse(_message.Message):
    __slots__ = ["name", "replicaServer"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    REPLICASERVER_FIELD_NUMBER: _ClassVar[int]
    name: str
    replicaServer: _CommWithReplica_pb2.Address
    def __init__(self, name: _Optional[str] = ..., replicaServer: _Optional[_Union[_CommWithReplica_pb2.Address, _Mapping]] = ...) -> None: ...
