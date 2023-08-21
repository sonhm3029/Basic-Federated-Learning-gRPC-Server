from concurrent import futures
import time
import numpy as np

import grpc
import greet_pb2
import greet_pb2_grpc

from ivirse.common.parameter import parameters_to_ndarrays, ndarrays_to_parameters
from ivirse.common.typing import Parameters
import struct


class GreeterService(greet_pb2_grpc.GreeterServicer):
    clients = []
    num_client = 0
    def SayHello(self, request_iterator, context):
        print("SayHello Request Made:")
        for request in request_iterator:
            print(request)
            hello_reply = greet_pb2.TestReply()
            hello_reply.msg = f"Xin chao {request.msg}"
        
            yield hello_reply
    
    def ParrotSaysHello(self, request, context):
        print("ParrotSayHello Request Made:")
        print(request)
        
        for i in range(3):
            hello_reply = greet_pb2.HelloReply()
            hello_reply.message = f"{request.greeting} {request.name} {i+1}"
            yield hello_reply
            time.sleep(3)
    
    def ChattyClientSaysHello(self, request_iterator, context):
        delayed_reply = greet_pb2.DelayedReply()
        for request in request_iterator:
            print("ChattyClientSayHello Request Made:")
            print(request)
            delayed_reply.request.append(request)
            
        delayed_reply.message = f"You have sent {len(delayed_reply.request)} message. Please expect a delayed Response"
        return delayed_reply
    

    def InteractingHello(self, request_iterator, context):
        try:
            print(context.peer())

            print(request_iterator)
            for request in request_iterator:
                print("InteractingHello Request Made:")
                parameters = request.parameters
                # Convert the received tensor bytes to a NumPy array
                print(len(parameters.tensors))
                tensor_bytes = parameters.tensors[0]  # Assuming only one tensor

                # Convert bytes to float array
                tensor_array = struct.unpack('f' * (len(tensor_bytes) // 4), tensor_bytes)

                # Process the tensor_array as needed
                tensor_array = [value / 2 for value in tensor_array]
                tensor_array = [struct.pack("f" * len(tensor_array), *tensor_array)]
                
                new_params = greet_pb2.Parameters(
                    tensors=tensor_array,
                    tensor_type="ND_REPLY"
                )

                # Create a HelloReply instance with the appropriate data
                yield greet_pb2.HelloReply(parameters=new_params)
        except Exception as e:
            print("STREAMMING ERROR",e)

    

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    greet_pb2_grpc.add_GreeterServicer_to_server(GreeterService(), server)
    
    server.add_insecure_port("0.0.0.0:50051")
    server.start()
    server.wait_for_termination()
    
if __name__ == "__main__":
    serve()