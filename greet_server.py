from concurrent.futures import ThreadPoolExecutor
import time
import numpy as np

import grpc
import greet_pb2
import greet_pb2_grpc

from ivirse.common.typing import Parameters
import struct

import asyncio
import threading


class GreeterService(greet_pb2_grpc.GreeterServicer):
    def __init__(self):
        self.clients = []
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)
        self.message = "Waiting for more clients..."
        self.params = []
        
            
    def InteractingHello(self, request_iterator, context):
        try:
            print(context.peer())
            with self.lock:
                self.clients.append(context)
                
                if len(self.clients) == 2:
                    self.message = "Start training"
                    self.condition.notify_all()
                else:
                    self.condition.wait()
                    
                response = greet_pb2.ServerReply(message = self.message)
                yield response
                
            
        except Exception as e:
            print("ERROR", e)
        # try:
        #     print(context.peer())

        #     print(request_iterator)
        #     for request in request_iterator:
        #         print("InteractingHello Request Made:")
        #         parameters = request.parameters/
        #         # Convert the received tensor bytes to a NumPy array
        #         print(len(parameters.tensors))
        #         tensor_bytes = parameters.tensors[0]  # Assuming only one tensor

        #         # Convert bytes to float array
        #         tensor_array = struct.unpack('f' * (len(tensor_bytes) // 4), tensor_bytes)

        #         # Process the tensor_array as needed
        #         tensor_array = [value / 2 for value in tensor_array]
        #         tensor_array = [struct.pack("f" * len(tensor_array), *tensor_array)]
                
        #         new_params = greet_pb2.Parameters(
        #             tensors=tensor_array,
        #             tensor_type="ND_REPLY"
        #         )

        #         # Create a HelloReply instance with the appropriate data
        #         yield greet_pb2.HelloReply(parameters=new_params)
        # except Exception as e:
        #     print("STREAMMING ERROR",e)

    

def serve():
    server = grpc.server(ThreadPoolExecutor(max_workers=2))
    greet_pb2_grpc.add_GreeterServicer_to_server(GreeterService(), server)
    
    server.add_insecure_port("0.0.0.0:50051")
    server.start()
    server.wait_for_termination()
    
    
if __name__ == "__main__":
    serve()