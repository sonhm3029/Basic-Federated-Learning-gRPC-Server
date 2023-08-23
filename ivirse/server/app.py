from .strategy import Strategy, FedAvg
from .client_manager import ClientManager, SimpleClientManager
from .history import History
from .server import Server
from ivirse.common.logger import log

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
    # grpc_server = 
    
    
    
    
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
        config = ServerConfig
    
    return server, config