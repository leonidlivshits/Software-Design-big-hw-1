from typing import List, Dict
from datetime import datetime
from Domain.Entities import Operation
from Services.Facades.analytics_strategies import BalanceDifferenceStrategy, CategoryGroupingStrategy
from .analytics_strategy import IAnalyticsStrategy
from Services.Repositories.repository import IRepository

class AnalyticsFacade:
    def __init__(self, operation_repo: IRepository[Operation]):
        self._repo = operation_repo
        self._strategies = {
            "balance": BalanceDifferenceStrategy(),
            "categories": CategoryGroupingStrategy()
        }

    def perform_analysis(self, analysis_type: str, 
                        start_date: datetime = None,
                        end_date: datetime = None) -> Dict[str, float]:
        operations = self._repo.get_all()
        strategy = self._strategies.get(analysis_type)
        if not strategy:
            raise ValueError(f"Unknown analysis type: {analysis_type}")
        return strategy.analyze(operations, start_date, end_date)

    def add_strategy(self, name: str, strategy: IAnalyticsStrategy):
        self._strategies[name] = strategy