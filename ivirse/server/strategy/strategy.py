from abc import ABC, abstractmethod
from typing import Optional, Tuple

from ivirse.server.client_manager import ClientManager
from ivirse.common.typing import Parameters


class Strategy(ABC):
    """Abstract base class for server strategy implementations"""
        
    @abstractmethod
    def configure_fit(
        self, sever_round: int, parameters: Parameters, client_manager: ClientManager
    ):
        """Configure the next round on training

        Args:
            sever_round (int): the current round of federated learning
            parameters (Parameters): The current (gloabal) model parameters
            client_manager (ClientManager): The client manager which holds all currently connected clients
        """