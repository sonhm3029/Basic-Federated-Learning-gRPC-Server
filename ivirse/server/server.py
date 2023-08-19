from concurrent import futures
import time

import grpc
from ivirse.proto import fl_pb2
from ivirse.proto import fl_pb2_grpc

from .client_proxy import ClientProxy

class FederatedService(fl_pb2_grpc.IvirseServiceServicer):
    
    num_client: int
    client = []
    
    def SendParams(self, request_iterator, context):
        for request