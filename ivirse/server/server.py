from ivirse.server.client_manager import ClientManager
from ivirse.server.history import History
from ivirse.common.logger import log
from ivirse.server.strategy import Strategy, FedAvg
from ivirse.server.client_proxy import ClientProxy
from ivirse.common.typing import Code, FitIns, FitRes, Parameters
from ivirse.common.parameter import parameters_to_ndarrays

from logging import DEBUG, INFO
import timeit

from typing import Optional, List, Tuple, Union
import numpy as np
import concurrent.futures


FitResultsAndFailures = Tuple[
    List[Tuple[ClientProxy, FitRes]],
    List[Union[Tuple[ClientProxy, FitRes], BaseException]],
]

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
        log(INFO, "FL starting!")
        start_time = timeit.default_timer() 
        
        for current_round in range(1, num_rounds + 1):
            res_fit = self.fit_round(server_round=current_round, timeout=timeout)
            if res_fit:
                parameters_prime, _ = res_fit
                if parameters_prime:
                    self.parameters = parameters_prime        
        # Bookkeeping
        end_time = timeit.default_timer()
        elapsed = end_time - start_time
        log(INFO, "FL finished in %s", elapsed)
        return history
    
    def fit_round(
        self,
        server_round: int,
        timeout: Optional[float]
    ) -> Optional[Tuple[Parameters, FitResultsAndFailures]]:
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
        
        # Collect `fit` results from all clients participating in this round
        results, failures = fit_clients(
            client_instructions=client_instructions,
            max_workers=self.max_workers,
            timeout=timeout
        )
        
        log(
            DEBUG,
            "fit_round %s received %s results and %s failures",
            server_round,
            len(results),
            len(failures)
        )
        
        # Aggregate training results
        parameters_aggregated: Optional[Parameters] = self.strategy.aggregate_fit(
            server_round=server_round,
            results=results,
            failures=failures
        )
        
        return parameters_aggregated, (results, failures)
        
        
        
    def _get_initial_parameters(self, timeout: Optional[float]) -> Parameters:
        """Get initial parameters from model save in server"""
        
        # Serverside parameters initialization
        parameters: Optional[Parameters] = self.strategy.initialize_parameters(
            client_manager=self._client_manager
        )
        if parameters is not None:
            log(INFO, "Using initial parameters provided by strategy")
            return parameters
        
        
        log(INFO, "Requesting initial parameters from one random client")
        random_client = self._client_manager.sample(1)[0]
        parameters = random_client.get_parameters(timeout=timeout)
        log(INFO, f"Received initial parameters from client: {random_client.cid}")
        
        return parameters
        
    
    # def disconnect_all_clients(self, timeout: Optional[float]) -> None:
    #     """Send shutdown signal to all clients."""
    #     all_clients = self._client_manager.all()
    #     clients = [all_clients[k] for k in all_clients.keys()]
    #     instruction = Re
    
def fit_clients(
    client_instructions: List[Tuple[ClientProxy, FitIns]],
    max_workers: Optional[int],
    timeout: Optional[float]
):
    """Refine parameters concurrently on all selected clients."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        submitted_fs = {
            executor.submit(fit_client, client_proxy, ins, timeout)
            for client_proxy, ins in client_instructions
        }
        
        finished_fs, _ =  concurrent.futures.wait(
            fs=submitted_fs,
            timeout=None
        )
        
        # Gather results
    results: List[Tuple[ClientProxy, FitRes]] = []
    failures: List[Union[Tuple[ClientProxy, FitRes], BaseException]] = []
    for future in finished_fs:
        _handle_finished_future_after_fit(
            future=future, results=results, failures=failures
        )
            
    return results, failures
            
def _handle_finished_future_after_fit(
    future: concurrent.futures.Future,
    results: List[Tuple[ClientProxy, FitRes]],
    failures: List[Union[Tuple[ClientProxy, FitRes], BaseException]]
) -> None:
    """Convert finished future into either a result or a failure"""

    # Check if there was an exception
    failure = future.exception()
    if failure is not None:
        failures.append(failure)
        return
    
    # Successfully received a result from a client
    result: Tuple[ClientProxy, FitRes] = future.result()
    _, res = result
    
    # check if result status code
    if res.status.code == Code.OK:
        results.append(result)
        return
    
    # Not successful, client returned a result where the status code is not OK
    failures.append(result)
    
def fit_client(
    client: ClientProxy,
    ins: FitIns,
    timeout: Optional[float]
) -> Tuple[ClientProxy, FitRes]:
    "Refine parameters on a single client."
    fit_res = client.fit(ins, timeout = timeout)
    return client, fit_res