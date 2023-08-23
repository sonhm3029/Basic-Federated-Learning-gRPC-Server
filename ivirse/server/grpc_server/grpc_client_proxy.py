from ..client_proxy import ClientProxy
from ivirse.server.grpc_server.grpc_bridge import GrpcBridge
from ivirse.server.grpc_server.grpc_bridge import ResWrapper, InsWrapper
from ivirse.common import FitRes, FitIns
from ivirse.common import serde

from ivirse.proto.transport_pb2 import ServerReply, ClientRequest

from typing import Optional

class GrpcClientProxy(ClientProxy):
    """ClientProxy that uses gRPC to delegate tasks over the network."""
    
    def __init__(
        self,
        cid: str,
        bridge: GrpcBridge
    ):
        super().__init__(cid)
        self.bridge = bridge
        
    def get_parameters(self, timeout: Optional[float]):
        """Return the current local model parameters."""
        print("THERS")
                
        res_wrapper: ResWrapper = self.bridge.request(
            ins_wrapper=InsWrapper(
                server_message=ServerReply(),
                timeout=timeout
            )
        )
        
        client_msg: ClientRequest = res_wrapper.client_message
        
        print(client_msg, "CLIENT_MSG")
        
        return []
        
    
    def fit(self,ins: FitIns,  timeout: Optional[float]):
        """Refine the provided parameters using the locally held datasets"""

        res_wrapper: ResWrapper = self.bridge.request(
            ins_wrapper=InsWrapper(
                server_message=ServerReply(parameters = FitIns.parameters),
                timeout=timeout
            )
        )
        client_msg: ClientRequest = res_wrapper.client_message
        fit_res = None
        return fit_res