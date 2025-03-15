from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List
from Domain.Entities import Operation

class IAnalyticsStrategy(ABC):
    @abstractmethod
    def analyze(self, operations: List[Operation], start_date: datetime = None, 
                end_date: datetime = None) -> Dict[str, float]:
        pass