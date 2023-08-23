from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod
from typing import Optional

from ivirse.common.typing import FitIns, FitRes


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
    def get_parameters(self, timeout: Optional[float]):
        """Return current local model parameters"""

    @abstractmethod
    def fit(
        self,
        ins: FitIns,
        timeout: Optional[float]
    ) -> FitRes:
        """Refine the provided parameters using locally held dataset."""