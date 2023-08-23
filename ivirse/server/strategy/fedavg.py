from .strategy import Strategy
from ivirse.common.logger import log
from ivirse.common.typing import Parameters
from ivirse.server.client_manager import ClientManager


from logging import WARNING
from typing import Tuple

WARNING_MIN_AVAILABLE_CLIENTS_TOO_LOW = """
Setting `min_available_clients` lower than `min_fit_clients` or
`min_evaluate_clients` can cause the server to fail when there are too few clients
connected to the server. `min_available_clients` must be set to a value larger
than or equal to the values of `min_fit_clients` and `min_evaluate_clients`.
"""

class FedAvg(Strategy):
    """Configurable FedAvg strategy implementation"""
    
    def __init__(
        self,
        *,
        faction_fit: float = 1.0,
        min_fit_clients: int = 2,
        min_available_clients: int = 2,
    ) -> None:
        """Federated Averaging Stategy.

        Args:
            faction_fit (float, optional):
                Fraction of clients used during training. In case `min_fit_clients`
                is larger than `fraction_fit * available_clients`, `min_fit_clients`
                will still be sampled.
                Defaults to 1.0.
            min_fit_clients (int, optional):
                Minimum number of clients used during training.
                Defaults to 2.
        """
        super().__init__()
        if (min_fit_clients > min_available_clients):
            log(WARNING, WARNING_MIN_AVAILABLE_CLIENTS_TOO_LOW)
            
        self.fraction_fit = faction_fit
        self.min_fit_clients = min_fit_clients
        self.min_available_clients = min_available_clients
        
    def num_fit_clients(self, num_available_clients: int) -> Tuple[int, int]:
        """
        Return the sample size and the required number of available clients.
        """
        num_clients = int(num_available_clients * self.fraction_fit)
        return max(num_clients, self.min_fit_clients), self.min_available_clients
    
    def configure_fit(
        self, server_round: int, parameters: Parameters, client_manager: ClientManager
    ):
        sample_size, min_num_clients = self.num_fit_clients(
            client_manager.num_available()
        )
        
        clients = client_manager.sample(
            num_clients=sample_size, min_num_clients=min_num_clients
        )
        
        return clients
    
    