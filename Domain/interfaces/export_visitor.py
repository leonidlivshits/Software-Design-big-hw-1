from abc import ABC, abstractmethod
from Domain.Entities import BankAccount, Category, Operation

class IExportVisitor(ABC):
    @abstractmethod
    def visit_bank_account(self, account: BankAccount) -> str:
        pass
    
    @abstractmethod
    def visit_category(self, category: Category) -> str:
        pass
    
    @abstractmethod
    def visit_operation(self, operation: Operation) -> str:
        pass