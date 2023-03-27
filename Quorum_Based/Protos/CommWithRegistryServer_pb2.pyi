import CommWithReplica_pb2 as _CommWithReplica_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ClientAddress(_message.Message):
    __slots__ = ["ip", "port"]
    IP_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    ip: str
    port: int
    def __init__(self, ip: _Optional[str] = ..., port: _Optional[int] = ...) -> None: ...

class QuorumParams(_message.Message):
    __slots__ = ["numReads", "numWrites", "totalReplicas"]
    NUMREADS_FIELD_NUMBER: _ClassVar[int]
    NUMWRITES_FIELD_NUMBER: _ClassVar[int]
    TOTALREPLICAS_FIELD_NUMBER: _ClassVar[int]
    numReads: int
    numWrites: int
    totalReplicas: int
    def __init__(self, totalReplicas: _Optional[int] = ..., numReads: _Optional[int] = ..., numWrites: _Optional[int] = ...) -> None: ...

class RegisterReplicaResponse(_message.Message):
    __slots__ = ["selfName", "status"]
    SELFNAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    selfName: str
    status: str
    def __init__(self, status: _Optional[str] = ..., selfName: _Optional[str] = ...) -> None: ...

class ReplicaListResponse(_message.Message):
    __slots__ = ["replicaServer"]
    REPLICASERVER_FIELD_NUMBER: _ClassVar[int]
    replicaServer: _CommWithReplica_pb2.Address
    def __init__(self, replicaServer: _Optional[_Union[_CommWithReplica_pb2.Address, _Mapping]] = ...) -> None: ...
