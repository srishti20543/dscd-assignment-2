# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: CommWithReplica.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15\x43ommWithReplica.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"1\n\x07\x41\x64\x64ress\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\n\n\x02ip\x18\x02 \x01(\t\x12\x0c\n\x04port\x18\x03 \x01(\x05\"\x1e\n\x0cStatusRepReq\x12\x0e\n\x06status\x18\x01 \x01(\t\";\n\x0cWriteRequest\x12\x0c\n\x04uuid\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\t\"c\n\x07Request\x12\x0c\n\x04uuid\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\t\x12+\n\x07version\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"\x1b\n\x0bReadRequest\x12\x0c\n\x04uuid\x18\x01 \x01(\t\"\x1d\n\rDeleteRequest\x12\x0c\n\x04uuid\x18\x01 \x01(\t\"S\n\x16\x44\x65leteRequestToReplica\x12\x0c\n\x04uuid\x18\x01 \x01(\t\x12+\n\x07version\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"Z\n\rWriteResponse\x12\x0e\n\x06status\x18\x01 \x01(\t\x12\x0c\n\x04uuid\x18\x02 \x01(\t\x12+\n\x07version\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"j\n\x0cReadResponse\x12\x0e\n\x06status\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\t\x12+\n\x07version\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp2\xa9\x03\n\x0f\x43ommWithReplica\x12,\n\x0fSendDetailsOfPR\x12\x08.Address\x1a\r.StatusRepReq\"\x00\x12(\n\x05Write\x12\r.WriteRequest\x1a\x0e.WriteResponse\"\x00\x12%\n\x04Read\x12\x0c.ReadRequest\x1a\r.ReadResponse\"\x00\x12)\n\x06\x44\x65lete\x12\x0e.DeleteRequest\x1a\r.StatusRepReq\"\x00\x12\x35\n\x13\x43onnectToPRforWrite\x12\r.WriteRequest\x1a\r.StatusRepReq\"\x00\x12\x37\n\x14\x43onnectToPRforDelete\x12\x0e.DeleteRequest\x1a\r.StatusRepReq\"\x00\x12\x35\n\x18\x43onnectToReplicaforWrite\x12\x08.Request\x1a\r.StatusRepReq\"\x00\x12\x45\n\x19\x43onnectToReplicaforDelete\x12\x17.DeleteRequestToReplica\x1a\r.StatusRepReq\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'CommWithReplica_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _ADDRESS._serialized_start=58
  _ADDRESS._serialized_end=107
  _STATUSREPREQ._serialized_start=109
  _STATUSREPREQ._serialized_end=139
  _WRITEREQUEST._serialized_start=141
  _WRITEREQUEST._serialized_end=200
  _REQUEST._serialized_start=202
  _REQUEST._serialized_end=301
  _READREQUEST._serialized_start=303
  _READREQUEST._serialized_end=330
  _DELETEREQUEST._serialized_start=332
  _DELETEREQUEST._serialized_end=361
  _DELETEREQUESTTOREPLICA._serialized_start=363
  _DELETEREQUESTTOREPLICA._serialized_end=446
  _WRITERESPONSE._serialized_start=448
  _WRITERESPONSE._serialized_end=538
  _READRESPONSE._serialized_start=540
  _READRESPONSE._serialized_end=646
  _COMMWITHREPLICA._serialized_start=649
  _COMMWITHREPLICA._serialized_end=1074
# @@protoc_insertion_point(module_scope)
