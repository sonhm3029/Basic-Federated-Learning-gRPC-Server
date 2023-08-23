from ..client_proxy import ClientProxy

from typing import Optional

class GrpcClientProxy(ClientProxy):
    """ClientProxy that uses gRPC to delegate tasks over the network."""
    
    def __init__(
        self,
        cid: str,
    ):
        super().__init__(cid)
        
    def get_parameters(self, timeout: Optional[float]):
        """Return the current local model parameters."""
        
    
    def fit(self, timeout: Optional[float]):
        """Refine the provided parameters using the locally held datasets"""
        