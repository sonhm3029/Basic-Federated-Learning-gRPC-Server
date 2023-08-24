from ivirse.proto.transport_pb2 import (
    ClientRequest,
    ServerReply,
    Parameters
)

from typing import List

from . import typing

def server_message_to_proto(server_message: typing.ServerReply) -> ServerReply:
    """Serialize `ServerReply` to ProtoBuf."""
    if server_message.parameters is not None:
        return ServerReply(parameters = parameters_to_proto(server_message.parameters))
    
    raise Exception("No parameters set in ServerReply, cannot serialize to Protobuf")
    
    
def parameters_to_proto(parameters: typing.Parameters) -> Parameters:
    """Serialize `Parameters` to ProtoBuf."""
    
    return Parameters(tensors=parameters.tensors, tensor_type=parameters.tensor_type)

def parameters_from_proto(msg: Parameters) -> typing.Parameters:
    """Deserialize `Parameters` from ProtoBuf."""
    # tensors: List[bytes] = list(msg.tensors)
    
    return typing.Parameters(tensors=msg.tensors, tensor_type=msg.tensor_type)

# def fit_res_from_proto(msg: )

