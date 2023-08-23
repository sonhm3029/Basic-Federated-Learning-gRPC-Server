from concurrent import futures
import time
from typing import Iterator, Callable
from iterators import TimeoutIterator

import grpc
from ivirse.proto import transport_pb2
from ivirse.proto import transport_pb2_grpc
from ivirse.proto.transport_pb2 import ClientRequest, ServerReply
from ivirse.server.grpc_server import GrpcClientProxy

from .client_proxy import ClientProxy
from .client_manager import ClientManager


def default_grpc_client_proxy_factory(cid: str) -> GrpcClientProxy:
    """Return GrpcClientProxy instance."""
    return GrpcClientProxy(cid=cid)

def register_client_proxy(
    client_manager: ClientManager,
    client_proxy: GrpcClientProxy,
    context: grpc.ServicerContext,
) -> bool:
    """Try registering GrpcClientProxy with ClientManager."""
    is_success = client_manager.register(client_proxy)
    if is_success:

        def rpc_termination_callback() -> None:
            client_manager.unregister(client_proxy)

        context.add_callback(rpc_termination_callback)
    return is_success

class IvirseServiceServicer(transport_pb2_grpc.TransportServicer):
    
    def __init__(
        self,
        client_manager: ClientManager,
    ) -> None:
        self.client_manager: ClientManager = client_manager
        self.client_proxy_factory = default_grpc_client_proxy_factory
        
    def Join(
        self,
        request_iterator: Iterator[ClientRequest],
        context: grpc.ServicerContext
    ) -> Iterator[ServerReply]:
        """
        Invoked by each gRPC client which participates in the network
        
        Protocol:
        - The first message is sent from the server to client
        - Both `ServerMessage` and `ClientMessage` are message "wrappers"
            wrapping the actual message
        
        """
        
        peer: str = context.peer()
        client_proxy= self.client_proxy_factory(peer)
        is_success = register_client_proxy(self.client_manager, client_proxy, context)
        
        if is_success:
            # Get Client request
            client_message_iterator = TimeoutIterator(
                iterator=request_iterator,
                reset_on_next=True
            )
            
            while True:
                try:
                    yield
                except StopIteration:
                    break
        
        