from logging import WARNING
from typing import Dict, List, Optional, Tuple, Union


from ivirse.common import (
    FitRes,
    Parameters,
    ndarrays_to_parameters,
    parameters_to_ndarrays
)

from ivirse.common.logger import log
from ivirse.common.typing import FitRes, Parameters
from ivirse.server.client_proxy import ClientProxy

from .aggregate import aggregate_median
from .fedavg import FedAvg



class FedMedian(FedAvg):
    """Configurable FedAvg with Momentum strategy implemetation."""
    
    def __repr__(self) -> str:
        """Compute a string representation of the strategy."""
        rep = f"FedMedian(accept_failures={self.accept_failures})"
        return rep
    
    def aggregate_fit(
        self,
        server_round: int,
        results: List[Tuple[ClientProxy, FitRes]],
        failures: List[Tuple[ClientProxy, FitRes] | BaseException]
    ) -> Parameters | None:
        """Aggregate fit results using median."""
        if not results:
            return None
        
        # Do not aggregate if there are failures and failures are not accepted
        if not self.accept_failures and failures:
            return None
        
        # Convert result
        weights_results= [
            parameters_to_ndarrays(fit_res.parameters)
            for _, fit_res in results
        ]
        
        parameter_aggregated = ndarrays_to_parameters(
            aggregate_median(weights_results)
        )
        
        return parameter_aggregated