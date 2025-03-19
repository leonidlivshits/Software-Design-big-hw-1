from collections import defaultdict
from typing import List, Dict
from datetime import datetime
from Domain.Entities import Operation
from Domain.enums.transaction_type import TransactionType
from Domain.interfaces.export_visitor import IExportVisitor
from Services.Facades.analytics_strategies import BalanceDifferenceStrategy, CategoryGroupingStrategy
from .analytics_strategy import IAnalyticsStrategy
from Services.Repositories.IRepository import IRepository

# class AnalyticsFacade:
#     def __init__(self, operation_repo: IRepository[Operation]):
#         self._repo = operation_repo
#         self._strategies = {
#             "balance": BalanceDifferenceStrategy(),
#             "categories": CategoryGroupingStrategy()
#         }

#     def perform_analysis(self, analysis_type: str, 
#                         start_date: datetime = None,
#                         end_date: datetime = None) -> Dict[str, float]:
#         operations = self._repo.get_all()
#         strategy = self._strategies.get(analysis_type)
#         if not strategy:
#             raise ValueError(f"Unknown analysis type: {analysis_type}")
#         return strategy.analyze(operations, start_date, end_date)

#     def add_strategy(self, name: str, strategy: IAnalyticsStrategy):
#         self._strategies[name] = strategy

#     def export_account(self, account_id: int, visitor: IExportVisitor) -> str:
#         account = self._repo.get(account_id)
#         if not account:
#             raise ValueError("Account not found")
#         return visitor.visit_bank_account(account)
    
class AnalyticsFacade:
    def __init__(self, operation_repo, account_repo, category_repo):
        self._category_repo = category_repo
        self._operation_repo = operation_repo
        self._account_repo = account_repo

    def get_balance_report(self, start: datetime, end: datetime) -> Dict:
        operations = self._filter_operations(start, end)
        
        income = sum(op.amount for op in operations if op.type == TransactionType.INCOME)
        expense = sum(op.amount for op in operations if op.type == TransactionType.EXPENSE)
        
        return {
            "income": income,
            "expense": expense,
            "balance": income - expense
        }

    def _filter_operations(self, start: datetime, end: datetime) -> List[Operation]:
        return [op for op in self._operation_repo.get_all() 
                if start <= op.date <= end]
    
    def get_category_report(self) -> Dict[str, float]:
        categories = {c.id: c for c in self._category_repo.get_all()}
        report = defaultdict(float)
        
        for op in self._operation_repo.get_all():
            if op.type == TransactionType.EXPENSE:
                category = categories.get(op.category_id)
                category_name = category.name if category else "Без категории"
                report[category_name] += op.amount
                
        return dict(report)