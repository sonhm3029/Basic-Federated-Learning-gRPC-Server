# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: fl.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x08\x66l.proto\x12\x08\x66l.proto\"7\n\x06Status\x12\x1c\n\x04\x63ode\x18\x01 \x01(\x0e\x32\x0e.fl.proto.Code\x12\x0f\n\x07message\x18\x02 \x01(\t\"2\n\nParameters\x12\x0f\n\x07tensors\x18\x01 \x03(\x0c\x12\x13\n\x0btensor_type\x18\x02 \x01(\t\"[\n\rClientMessage\x12 \n\x06status\x18\x01 \x01(\x0b\x32\x10.fl.proto.Status\x12(\n\nparameters\x18\x02 \x01(\x0b\x32\x14.fl.proto.Parameters\"9\n\rServerMessage\x12(\n\nparameters\x18\x01 \x01(\x0b\x32\x14.fl.proto.Parameters*[\n\x06Reason\x12\x0b\n\x07UNKNOWN\x10\x00\x12\r\n\tRECONNECT\x10\x01\x12\x16\n\x12POWER_DISCONNECTED\x10\x02\x12\x14\n\x10WIFI_UNAVAILABLE\x10\x03\x12\x07\n\x03\x41\x43K\x10\x04*\x19\n\x04\x43ode\x12\x06\n\x02OK\x10\x00\x12\t\n\x05\x45RROR\x10\x01\x32M\n\rIvirseService\x12<\n\x04Join\x12\x17.fl.proto.ClientMessage\x1a\x17.fl.proto.ServerMessage(\x01\x30\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'fl_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _globals['_REASON']._serialized_start=283
  _globals['_REASON']._serialized_end=374
  _globals['_CODE']._serialized_start=376
  _globals['_CODE']._serialized_end=401
  _globals['_STATUS']._serialized_start=22
  _globals['_STATUS']._serialized_end=77
  _globals['_PARAMETERS']._serialized_start=79
  _globals['_PARAMETERS']._serialized_end=129
  _globals['_CLIENTMESSAGE']._serialized_start=131
  _globals['_CLIENTMESSAGE']._serialized_end=222
  _globals['_SERVERMESSAGE']._serialized_start=224
  _globals['_SERVERMESSAGE']._serialized_end=281
  _globals['_IVIRSESERVICE']._serialized_start=403
  _globals['_IVIRSESERVICE']._serialized_end=480
# @@protoc_insertion_point(module_scope)