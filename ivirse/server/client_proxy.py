from dataclasses import dataclass
from enum import Enum


class BatteryStatus(Enum):
    PLUG: bool

@dataclass
class Properties:
    battery_status: BatteryStatus
    

class ClientProxy:
    def __init__(self, cid: str, properties: Properties, parameters):
        self.cid = cid
        self.properties = properties
        self.parameters = parameters
        
    def get_properties(self):
        return self.properties
    
    def get_parameters(self):
        return self.parameters
