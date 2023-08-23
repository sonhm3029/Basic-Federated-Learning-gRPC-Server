from ivirse.server.client_manager import ClientManager
from ivirse.server.history import History
from ivirse.common.logger import log
from ivirse.server.strategy import Strategy, FedAvg
from ivirse.server.client_proxy import ClientProxy
from ivirse.common.typing import Code

from logging import DEBUG, INFO
import timeit

from typing import Optional, List
import numpy as np
import concurrent.futures

class Server:
    """Ivirse server."""
    def __init__(
        self, *, client_manager: ClientManager, strategy: Optional[Strategy]
    ) -> None:
        self._client_manager: ClientManager = client_manager
        self.parameters = []
        self.max_workers: Optional[int] = None
        self.strategy: Strategy = strategy if strategy is not None else FedAvg()
        
    def set_max_workers(self, max_workers: Optional[int]) -> None:
        """Set the max_workers used by ThreadPoolExecutor"""
        self.max_workers = max_workers
        
    def client_manager(self) -> ClientManager:
        """Return ClientManager"""
        return self._client_manager
    
    def fit(self, num_rounds: int, timeout: Optional[float]) -> History:
        history = History()
        
        log(INFO, "Initialize global parameters")
        self.parameters = self._get_initial_parameters(timeout=timeout)
        
        # Training
        log(INFO, "Start training")
        start_time = timeit.default_timer() 
        
        for current_round in range(1, num_rounds + 1):
            res_fit = self.fit_round(server_round=current_round, timeout=timeout)
    
    def fit_round(
        self,
        server_round: int,
        timeout: Optional[float]
    ):
        """Perform a single round of federated averaging"""
        
        # Get clients and their respective instructions
        client_instructions =  self.strategy.configure_fit(
            server_round=server_round,
            parameters=self.parameters,
            client_manager=self._client_manager
        )
        
        if not client_instructions:
            log(INFO, "Fit round %s: no clients selected, cancel", server_round)
            return None
        log(
            DEBUG,
            "Fit round %s: strategy sampled %s clients(out of %s)",
            server_round,
            len(client_instructions),
            self._client_manager.num_available()
        )
        
        
        
    def _get_initial_parameters(self, timeout: Optional[float]):
        """Get initial parameters from model save in server"""
        parameters = np.random.rand(1280)
        return parameters
    
def fit_clients(
    client_instructions,
    max_workers: Optional[int],
    timeout: Optional[float]
):
    """Refine parameters concurrently on all selected clients."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        submitted_fs = {
            executor.submit(fit_client, client_proxy, timeout)
            for client_proxy in client_instructions
        }
        
        finished_fs, _ =  concurrent.futures.wait(
            fs=submitted_fs,
            timeout=None
        )
        
        # Gather results
    results: List[ClientProxy] = []
    for future in finished_fs:
        _handle_finished_future_after_fit(
            future=future, results=results
        )
            
    return results
            
def _handle_finished_future_after_fit(
    future: concurrent.futures.Future,
    results: List[ClientProxy]
) -> None:
    """Convert finished future into either a result or a failure"""

    # Check if there was an exception
    
    
    # Successfully received a result from a client
    result: ClientProxy = future.result()
    _, res = result
    
    # check if result status code
    if res.status.code == Code.OK:
        results.append(result)
        return
    
def fit_client(
    client: ClientProxy,
    timeout: Optional[float]
):
    "Refine parameters on a single client."
    fit_res = client.fit(timeout = timeout)
    return client, fit_res