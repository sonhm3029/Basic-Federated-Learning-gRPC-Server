from ivirse.server.client_manager import ClientManager
import grpc

def start_grpc_server(
    client_manager: ClientManager,
    server_address: str,
    max_concurrent_workers: int = 1000,
    keepalive_time_ms: int = 210000
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
    
    # servicer = 
    