from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod
from typing import Optional


class BatteryStatus(Enum):
    PLUG: bool

@dataclass
class Properties:
    battery_status: BatteryStatus
    

class ClientProxy(ABC):
    """Abstract base class for client proxies"""
    
    def __init__(self, cid: str):
        self.cid = cid
        
    
    @abstractmethod
    def get_parameters(self):
        """Return current local model parameters"""

    @abstractmethod
    def fit(
        self,
        timeout: Optional[float]
    ):
        """Refine the provided parameters using locally held dataset."""