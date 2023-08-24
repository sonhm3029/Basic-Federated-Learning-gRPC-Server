from ..client_proxy import ClientProxy
from ivirse.server.grpc_server.grpc_bridge import GrpcBridge
from ivirse.server.grpc_server.grpc_bridge import ResWrapper, InsWrapper
from ivirse.common import FitRes, FitIns
from ivirse.common import serde
from ivirse.common.parameter import parameters_to_ndarrays, ndarrays_to_parameters

from ivirse.proto.transport_pb2 import ServerReply, ClientRequest

from typing import Optional
from ivirse.common.typing import Status, Code

class GrpcClientProxy(ClientProxy):
    """ClientProxy that uses gRPC to delegate tasks over the network."""
    
    def __init__(
        self,
        cid: str,
        bridge: GrpcBridge
    ):
        super().__init__(cid)
        print(f"Device {cid} connected!")
        self.bridge = bridge
        
    def get_parameters(self, timeout: Optional[float]):
        """Return the current local model parameters."""
                
        res_wrapper: ResWrapper = self.bridge.request(
            ins_wrapper=InsWrapper(
                server_message=ServerReply(message="Request parameters"),
                timeout=timeout
            )
        )
        
        client_msg: ClientRequest = res_wrapper.client_message
        
        parameters = serde.parameters_from_proto(client_msg.parameters)
                
        return parameters
        
    
    def fit(self,ins: FitIns,  timeout: Optional[float]):
        """Refine the provided parameters using the locally held datasets"""

        parameters = serde.parameters_to_proto(ins.parameters)
        
        res_wrapper: ResWrapper = self.bridge.request(
            ins_wrapper=InsWrapper(
                server_message=ServerReply(parameters = parameters),
                timeout=timeout
            )
        )
        client_msg: ClientRequest = res_wrapper.client_message        
        return FitRes(
            parameters=serde.parameters_to_proto(client_msg.parameters),
            status=Status(
                code = Code.OK,
                message="OK"
            )
        )