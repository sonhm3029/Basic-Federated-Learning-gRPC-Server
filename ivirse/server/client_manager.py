from abc import ABC, abstractmethod
from typing import Dict



class ClientManager(ABC):
    @abstractmethod
    def num_available(self) -> int:
        """Return the number of available clients.

        Returns:
        ________
        num_available : int
            The number of currently available clients.
        """
        
    @abstractmethod
    def all(self) -> Dict[str, ClientProxy]:
        """Return all available clients"""
        