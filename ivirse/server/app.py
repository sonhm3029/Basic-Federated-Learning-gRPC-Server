from .strategy import Strategy, FedAvg
from .client_manager import ClientManager, SimpleClientManager
from .history import History
from .server import Server
from ivirse.common.logger import log
from ivirse.server.grpc_server.grpc_server import start_grpc_server
from ivirse.common.grpc import GRPC_MAX_MESSAGE_LENGTH

from typing import Optional
from dataclasses import dataclass
from logging import INFO

@dataclass
class ServerConfig:
    """Server config"""
    num_rounds: int = 1
    round_timeout: Optional[float] = None

def start_server(
    *,
    server_address: str,
    config: Optional[ServerConfig] = None,
    strategy: Optional[Strategy] = None,
    client_manager: Optional[ClientManager] = None,
    grpc_max_message_length: int = GRPC_MAX_MESSAGE_LENGTH
) -> History:
    # Initialize server
    initialized_server, initialized_config = _init_defaults(
        config = config,
        strategy=strategy,
        client_manager=client_manager
    )
    log(
        INFO,
        "Start Federated learning server, config: %s",
        initialized_config
    )
    
    # Start grpc Server
    grpc_server = start_grpc_server(
        client_manager=initialized_server.client_manager(),
        server_address=server_address,
        max_message_length=grpc_max_message_length
    )
    
    log(
        INFO,
        "gRPC server running (%s rounds)",
        initialized_config.num_rounds
    )
    
    # Start training
    hist = _fl(
        server=initialized_server,
        config=initialized_config,
    )
    
    
    # Stop the gRPC server
    grpc_server.stop(grace=1)
    
    return hist
    
    
def _init_defaults(
    strategy: Optional[Strategy],
    client_manager: Optional[ClientManager],
    config: Optional[ServerConfig]
):
    if client_manager is None:
        client_manager = SimpleClientManager()
    if strategy is None:
        strategy = FedAvg()
        
    server = Server(
        client_manager=client_manager,
        strategy=strategy
    )
    
    if config is None:
        config = ServerConfig()
    
    return server, config


def _fl(
    server: Server,
    config: ServerConfig
) -> History:
    # Fit model
    hist = server.fit(num_rounds=config.num_rounds, timeout=config.round_timeout)
    
    # server.disconnect_all_clients(timeout=config.round_timeout)
    return hist