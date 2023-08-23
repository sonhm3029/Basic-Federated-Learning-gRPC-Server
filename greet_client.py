import greet_pb2_grpc
import greet_pb2
import grpc

import time
import numpy as np
import sys

from ivirse.common.parameter import ndarrays_to_parameters, parameters_to_ndarrays
from ivirse.common.typing import Parameters                                 

from ivirse.proto import transport_pb2, transport_pb2_grpc

def write_bytes_list_to_file(bytes_list, filename):
    with open(filename, "wb") as f:
        for item in bytes_list:
            f.write(item)

def get_client_stream_requests():
    while True:
        name = input("Please enter a name (or nothing to stop chatting): ")
        
        if name == "":
            break
        
        arr = np.random.rand(1280)
        parameters = ndarrays_to_parameters(
            arr
        )
        print(f"Request raw size : {arr.nbytes / 1000} KB")
        parameters = greet_pb2.Parameters(tensors=parameters.tensors,
                                         tensor_type=parameters.tensor_type)
        hello_request = greet_pb2.HelloRequest(parameters=parameters)
        serialized_request = hello_request.SerializeToString()
        request_size_bytes = len(serialized_request) /1000
        print(f"Request size : {request_size_bytes} KB")
        yield hello_request

def run():

    with grpc.insecure_channel('localhost:50051') as channel:
        stub= transport_pb2_grpc.TransportStub(channel)

        
        responses = stub.Join(get_client_stream_requests())
        for response in responses:
            print("InteractingHello Response Received: ")
            end = time.time()
            print("Received time: ", end)
            # parameters = parameters_to_ndarrays(
            #     Parameters(tensors=response.parameters.tensors,
            #                tensor_type=response.parameters.tensor_type)
            # )
            
                
        
        
if __name__ == "__main__":
    run()