from io import BytesIO
from typing import cast

import numpy as np
import struct

from .typing import Parameters, NDArray, NDArrays

def ndarrays_to_parameters(ndarrays: NDArrays) -> Parameters:
    """Convert Numpy ndarrays to paremeters object"""
    tensors = [ndarray_to_bytes_v2(ndarray) for ndarray in ndarrays]
    return Parameters(tensors=tensors, tensor_type="numpy.ndarray")

def parameters_to_ndarrays(parameters: Parameters) -> NDArrays:
    """Convert parameters object to Numpy ndarrays"""
    return [bytes_to_ndarray_v2(tensor) for tensor in parameters.tensors]  


    
def ndarray_to_bytes(ndarray: NDArray) -> bytes:
    """Serialize Numpy ndarray to bytes."""
    bytes_io = BytesIO()
    # WARNING: NEVER set allow_pickle to true
    # Reason: loading pickled data can execute arbitrary code
    # Source: https://numpy.org/doc/stable/reference/generated/numpy.save.html
    np.save(bytes_io, ndarray, allow_pickle=False) #type: ignore
    return bytes_io.getvalue()

def bytes_to_ndarray(tensor: bytes) -> NDArray:
    """Deserialize Numpy ndarray from bytes"""
    bytes_io = BytesIO(tensor)
    
    ndarray_deserialized = np.load(bytes_io, allow_pickle=False)
    return cast(NDArray, ndarray_deserialized)

def bytes_to_ndarray_v2(tensor_bytes: bytes) -> NDArray:
    """Deserialize Numpy ndarray from bytes"""
    tensor_array = struct.unpack('f' * (len(tensor_bytes) // 4), tensor_bytes)
    
    return np.array(tensor_array)

def ndarray_to_bytes_v2(tensor_array: NDArray) -> bytes:
    """Serialize Numpy ndarray to bytes."""
    tensor_array = tensor_array.tolist()
    tensor_array = struct.pack("f" * len(tensor_array), *tensor_array)
    
    return tensor_array