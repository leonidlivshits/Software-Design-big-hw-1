from datetime import datetime
from collections import defaultdict
from typing import Dict, List
from Domain.Entities import Operation
from Domain.enums import TransactionType
from .analytics_strategy import IAnalyticsStrategy

class BalanceDifferenceStrategy(IAnalyticsStrategy):
    def analyze(self, operations: List[Operation], start_date: datetime = None, 
                end_date: datetime = None) -> Dict[str, float]:
        filtered = self._filter_by_date(operations, start_date, end_date)
        income = sum(op.amount for op in filtered if op.type == TransactionType.INCOME)
        expense = sum(op.amount for op in filtered if op.type == TransactionType.EXPENSE)
        return {"income": income, "expense": expense, "difference": income - expense}

class CategoryGroupingStrategy(IAnalyticsStrategy):
    def analyze(self, operations: List[Operation], start_date: datetime = None,
                end_date: datetime = None) -> Dict[str, float]:
        filtered = self._filter_by_date(operations, start_date, end_date)
        result = defaultdict(float)
        for op in filtered:
            result[op.category_id] += op.amount
        return dict(result)

    @staticmethod
    def _filter_by_date(ops: List[Operation], start: datetime, end: datetime):
        if not start and not end:
            return ops
        return [op for op in ops if (not start or op.date >= start) and (not end or op.date <= end)]