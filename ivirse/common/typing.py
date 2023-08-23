from dataclasses import dataclass
from typing import List, Dict, Union, Optional, Any
from enum import Enum
import numpy.typing as npt

Scalar = Union[bool, bytes, float, int, str]
NDArray = npt.NDArray[Any]
NDArrays = List[NDArray]


Properties = Dict[str, Scalar]
Config = Dict[str, Scalar]

class Code(Enum):
    """Client status code."""
    OK = 0

@dataclass
class Parameters:
    """Model parameters."""
    tensors: List[bytes]
    tensor_type: str
    
@dataclass
class Status:
    """Client status."""
    
    code: Code
    message: str
    
    
@dataclass
class FitIns:
    """Fit instructions for a client."""
    
    parameters: Parameters   

@dataclass
class FitRes:
    """Fit response from a client."""
    parameters: Parameters
    status: Status


@dataclass
class ServerReply:
    """ServerReply is a container used to hold one instruction message."""
    parameters: Optional[Parameters] = None
    

@dataclass
class ClientRequest:
    """ClientRequest is a container used to hold one result message."""
    parameters: Optional[Parameters] = None
@dataclass
class GetPropertiesIns:
    """Properties request for a client."""
    
    config: Config
    
@dataclass
class GetPropertiesRes:
    """Properties response from a client."""
    
    status: Status
    properties: Properties
    
@dataclass
class GetParametersIns:
    """Parameters request for a client."""
    
    config: Config
    
@dataclass
class GetParametersRes:
    """Response when asked to return parameters"""
    
    status: Status
    parameters: Parameters
    
@dataclass 
class ReconnectIns:
    """ReconnectIns message from server to client."""
    
    seconds: Optional[int]
    
@dataclass
class DisconnectRes:
    """DisconnectRes message from client to server"""    
    reason: str
    
    