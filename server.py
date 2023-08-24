from ivirse.server.app import start_server
from ivirse.server.strategy import FedAvg
import ivirse

strategy = FedAvg(
    faction_fit=1.0,
    min_fit_clients=2,
    min_available_clients=2
)

start_server(
    server_address="0.0.0.0:50051",
    strategy= strategy,
    config=ivirse.server.ServerConfig(num_rounds=4)
)