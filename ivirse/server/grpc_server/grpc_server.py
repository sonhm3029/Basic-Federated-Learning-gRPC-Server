from ivirse.server.client_manager import ClientManager
from ivirse.server.FederatedService import IvirseServiceServicer
from ivirse.proto.transport_pb2_grpc import add_TransportServicer_to_server
from ivirse.common.grpc import GRPC_MAX_MESSAGE_LENGTH

import grpc
from concurrent.futures import ThreadPoolExecutor

from typing import Optional, Callable, Any, Tuple


AddServicerToServerFn = Callable[..., Any]

def start_grpc_server(
    client_manager: ClientManager,
    server_address: str,
    max_concurrent_workers: int = 1000,
    keepalive_time_ms: int = 210000,
    max_message_length: int = GRPC_MAX_MESSAGE_LENGTH
) -> grpc.Server:
    """Create and start a gRPC server running FederatedServiceServicer.
    
    If used in a main function server.wait_for_termination(timeout=None)
    should be called as otherwise the server will immediately stop.

    Args:
        client_manager (ClientManager): ClientManager
        server_address (str):
            Server address in the form of HOST:PORT e.g "[::]:8080"
        max_concurrent_workers (int, optional):
            Maximum number of clients the server can process before returning
            RESOURCE_EXHAUSTED status (default: 1000)
        keepalive_time_ms (int, optional):
            Defaults to 210000 (3m 3s).

    Returns:
        grpc.Server:
            An instance of a gRPC server which is already started
    """
    
    servicer = IvirseServiceServicer(client_manager)
    add_service_to_server_fn = add_TransportServicer_to_server
    
    server = generic_create_grpc_server(
        servicer_and_add_fn=(servicer, add_service_to_server_fn),
        server_address=server_address,
        max_concurrent_workers=max_concurrent_workers,
        max_message_length=max_message_length,
        keepalive_time_ms=keepalive_time_ms
    )
    
    server.start()
    # server.wait_for_termination()
    
    return server
    
    
def generic_create_grpc_server(
    servicer_and_add_fn: Tuple[IvirseServiceServicer, AddServicerToServerFn],
    server_address: str,
    max_concurrent_workers: int = 1000,
    keepalive_time_ms: int = 210000,
    max_message_length: int = GRPC_MAX_MESSAGE_LENGTH,
) -> grpc.Server:
    """Generic function to create a gRPC server with a single servicer

    Args:
        servicer_and_add_fn (Tuple[IvirseServiceServicer, AddServicerToServerFn]): 
            A tuple holding a servicer implementation and a matching add_Servicer_to_server funtion
        server_address (str): 
            Server address in the form of HOST: PORT e.g "[::]:8000"
        max_concurrent_workers (int, optional): 
            Maximum number of clients the server can process before returning RESOURCE_EXHAUSTED status. Defaults to 1000.
            keepalive_time_ms (int, optional): Defaults to 210000.

    Returns:
        grpc.Server: A non-running instance of a gRPC server.
    """
    servicer, add_servicer_to_server_fn = servicer_and_add_fn
    
    options = [
        # Maximum number of concurrent incoming streams to allow on a http2
        # connection. Int valued.
        ("grpc.max_concurrent_streams", max(100, max_concurrent_workers)),
        # Maximum message length that the channel can send.
        # Int valued, bytes. -1 means unlimited.
        ("grpc.max_send_message_length", max_message_length),
        # Maximum message length that the channel can receive.
        # Int valued, bytes. -1 means unlimited.
        ("grpc.max_receive_message_length", max_message_length),
        # The gRPC default for this setting is 7200000 (2 hours). Flower uses a
        # customized default of 210000 (3 minutes and 30 seconds) to improve
        # compatibility with popular cloud providers. Mobile Flower clients may
        # choose to increase this value if their server environment allows
        # long-running idle TCP connections.
        ("grpc.keepalive_time_ms", keepalive_time_ms),
        # Setting this to zero will allow sending unlimited keepalive pings in between
        # sending actual data frames.
        ("grpc.http2.max_pings_without_data", 0),
    ]
    
    server = grpc.server(
        ThreadPoolExecutor(max_workers=max_concurrent_workers),
        maximum_concurrent_rpcs=max_concurrent_workers,
        options=options
    )
    
    add_servicer_to_server_fn(servicer, server)
    
    
    server.add_insecure_port(server_address)
    
    return server