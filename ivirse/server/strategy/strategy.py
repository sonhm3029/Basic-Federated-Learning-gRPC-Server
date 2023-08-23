from abc import ABC, abstractmethod
from typing import Optional, Tuple, List, Union, Dict

from ivirse.server.client_manager import ClientManager
from ivirse.common.typing import Parameters, FitRes
from ivirse.server.client_proxy import ClientProxy


class Strategy(ABC):
    """Abstract base class for server strategy implementations"""
        
    
    @abstractmethod
    def initialize_parameters(
        self, client_manager: ClientManager
    ) -> Optional[Parameters]:
        """Initialize the (global) model parameters

        Args:
            client_manager (ClientManager):
                The client manager which holds all currently connected clients

        Returns:
            Optional[Parameters]:
                If parameters are returned, then the server will treat these
                as the initial global model parameters
        """
        
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
        
    @abstractmethod
    def aggregate_fit(
        self,
        server_round: int,
        results: List[Tuple[ClientProxy, FitRes]],
        failures: List[Union[Tuple[ClientProxy, FitRes], BaseException]]
    ) -> Optional[Parameters]:
        """Aggregate training results

        Args:
            server_round (int): 
                The current round of federated learning.
            results (List[Tuple[ClientProxy, FitRes]]):
                Successful updates from the previously selected and configured
                clients. Each pair of `(ClientProxy, FitRes)` constitues a 
                successful update from one of the previous selected clients. Not
                that not all previously selected clients are necessarily included in
                this list: a client might drop out and not submit a result. For each client
                that did not submit an update, there should be an `Exception`
                in `failures`
            failures (List[Union[Tuple[ClientProxy, FitRes], BaseException]]):
                Exceptions that occurred while the server was waiting for client
                updates.

        Returns:
            Optional[Parameters]:
                If parameters are returned, then the server will treat these as the
                new global model parameters (i.e., it will replace the previous parameters
                with the ones returned from this method). If `None` is returned
                (e.g, becuase there were only failures and no viable results)
                then the server will no update the previous model parameters,
                the updates received in this round are discarded, and the global
                model parameters remain the same.
        """