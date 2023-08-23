from concurrent import futures
import time
from typing import Iterator, Callable
from iterators import TimeoutIterator

import grpc
from ivirse.proto import transport_pb2
from ivirse.proto import transport_pb2_grpc
from ivirse.proto.transport_pb2 import ClientRequest, ServerReply
from ivirse.server.grpc_server import GrpcClientProxy, GrpcBridge
from ivirse.server.grpc_server.grpc_bridge import InsWrapper, ResWrapper

from .client_proxy import ClientProxy
from .client_manager import ClientManager


def default_bridge_factory() -> GrpcBridge:
    """Return GrpcBridge instance."""
    return GrpcBridge()

def default_grpc_client_proxy_factory(cid: str, bridge: GrpcBridge) -> GrpcClientProxy:
    """Return GrpcClientProxy instance."""
    return GrpcClientProxy(cid=cid, bridge=bridge)

def register_client_proxy(
    client_manager: ClientManager,
    client_proxy: GrpcClientProxy,
    context: grpc.ServicerContext,
) -> bool:
    """Try registering GrpcClientProxy with ClientManager."""
    is_success = client_manager.register(client_proxy)
    if is_success:

        def rpc_termination_callback() -> None:
            client_proxy.bridge.close()
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
        self.grpc_bridge_factory = default_bridge_factory
        
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
        bridge = self.grpc_bridge_factory()
        client_proxy= self.client_proxy_factory(peer, bridge)
        is_success = register_client_proxy(self.client_manager, client_proxy, context)
        
        if is_success:
            # Get Client request
            client_message_iterator = TimeoutIterator(
                iterator=request_iterator,
                reset_on_next=True
            )
            ins_wrapper_iterator = bridge.ins_wrapper_iterator()
            
            # All messages will be pushed to client bridge directly
            while True:
                try:
                    # Get ins_wrapper from bridge and yield server_message
                    ins_wrapper: InsWrapper = next(ins_wrapper_iterator)
                    yield ins_wrapper.server_message
                    
                    # Set current timour, might be None
                    if ins_wrapper.timeout is not None:
                        client_message_iterator.set_timeout(ins_wrapper.timeout)
                        
                    # Wait for client message
                    client_message = next(client_message_iterator)
                    
                    if client_message is client_message_iterator.get_sentinel():
                        # Importatnt: calling `context.abort` in gRPC always
                        # raises an exception so that all code after call to
                        # `context.abort` will not run. If subsequent code should
                        #  be executed, the `rpc_termination_callback` can be used
                        # (as shown in the `register_client` function).
                        details = f"Timeout of {ins_wrapper.timeout} sec was exceeded."
                        context.abort(
                            code=grpc.StatusCode.DEADLINE_EXCEEDED,
                            details=details
                        )
                    
                    bridge.set_res_wrapper(
                        res_wrapper=ResWrapper(client_message=client_message)
                    )
                    
                except StopIteration:
                    break
        
        