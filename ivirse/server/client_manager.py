from abc import ABC, abstractmethod
from typing import Dict, Optional, List
from dataclasses import dataclass
import threading
import random

from ivirse.server.client_proxy import ClientProxy



class ClientManager(ABC):
    """Abstract base class for managing Flower clients."""
    @abstractmethod
    def num_available(self) -> int:
        """Return the number of available clients

        Returns:
            int: num_available
                The number of currently available clients.
        """
    
    @abstractmethod
    def register(self, client: ClientProxy) -> bool:
        """Register ClientProxy instance

        Args:
            client (ClientProxy): ivirse.server.client_proxy.ClientProxy

        Returns:
            bool: success
                Indicating if registration was successful. False if ClientProxy is
                already registered or can not be registered for any reason
        """
    
    @abstractmethod
    def unregister(self, client: ClientProxy) -> None:
        """Unregister ClientProxy instance.

        Args:
            client (ClientProxy): ivirse.server.client_proxy.ClientProxy
        """
    
    @abstractmethod
    def all(self) -> Dict[str, ClientProxy]:
        """Return all available clients.
        """
    
    @abstractmethod
    def wait_for(self, num_clients: int, timeout: int) -> bool:
        """Wait until at least `num_clients` are available."""
        
    @abstractmethod
    def sample(
        self,
        num_clients: int,
        min_num_clients: Optional[int] = None,
    ) -> List[ClientProxy]:
        """
            Sample a number of ClientProxy instances.
        """
        
        
class SimpleClientManager(ClientManager):
    """Provides a pool of available clients."""
    
    def __init__(self) -> None:
        self.clients: Dict[str, ClientProxy] = {}
        self._cv = threading.Condition()
         
    def __len__(self) -> int:
        return len(self.clients)
    
    def num_available(self) -> int:
        """Return the number of available clients

        Returns:
            int: num_available
                The number of currently available clients.
        """
        return len(self)
    
    def register(self, client: ClientProxy) -> bool:
        """Register ClientProxy instance

        Args:
            client (ClientProxy): ivirse.server.client_proxy.ClientProxy

        Returns:
            bool: success
                Indicating if registration was successful. False if ClientProxy is
                already registered or can not be registered for any reason
        """
        if client.cid in self.clients:
            return False
        self.clients[client.cid] = client
        with self._cv:
            self._cv.notify_all()
            
        return True
    
    def unregister(self, client: ClientProxy) -> None:
        """Unregister ClientProxy instance.

        Args:
            client (ClientProxy): ivirse.server.client_proxy.ClientProxy
        """
        if client.cid in self.clients:
            del self.clients[client.cid]
            
            with self._cv:
                self._cv.notify_all()
    
    def all(self) -> Dict[str, ClientProxy]:
        """Return all available clients.
        """
        return self.clients
    
    def wait_for(self, num_clients: int, timeout: int = 86400) -> bool:
        """Wait until at least `num_clients` are available.
        
        Blocks until the requested number of clients is available or until a
        timeout is reached. Current timeout default: 1 day.

        Args:
            num_clients (int): The number of clients to wait for.
            timeout (int): The time in seconds to wait for, defaults to 86400 (24h)

        Returns:
            bool: success
        """
        with self._cv:
            return self._cv.wait_for(
                lambda: len(self.clients) >= num_clients, timeout=timeout
            )
        
    def sample(
        self,
        num_clients: int,
        min_num_clients: Optional[int] = None,
    ) -> List[ClientProxy]:
        """
            Sample a number of ClientProxy instances.
        """
        # Block until at least num_clients are connected.
        if min_num_clients is None:
            min_num_clients  = num_clients
        self.wait_for(min_num_clients)
        
        # Sample clients which meet the criterion
        available_cids = list(self.clients)

        if num_clients > len(available_cids):
            return []
        
        sampled_cids = random.sample(available_cids, num_clients)
        return [self.clients[cid] for cid in sampled_cids]
