from typing import List
from Domain.Entities import Operation
from Domain.Entities.Category import Category
from Domain.enums.transaction_type import TransactionType
from Services.Facades.account_facade import AccountFacade
from Services.Repositories.IRepository import IRepository

# class OperationFacade:
#     def __init__(self, operation_repo: IRepository[Operation]):
#         self._repo = operation_repo

#     def create_operation(self, operation: Operation) -> Operation:
#         if operation.amount <= 0:
#             raise ValueError("Amount must be positive")
#         self._repo.add(operation)
#         return operation

#     def get_operations_by_account(self, account_id: int) -> List[Operation]:
#         return [op for op in self._repo.get_all() if op.bank_account_id == account_id]

#     def delete_operation(self, operation_id: int) -> None:
#         self._repo.remove(operation_id)

#     def get_all_operations(self) -> List[Operation]:
#         return self._repo.get_all()
    
class OperationFacade:
    def __init__(self, 
                 operation_repo: IRepository[Operation],
                 account_facade: AccountFacade):
        self._repo = operation_repo
        self._account_facade = account_facade

    def create_operation(self, operation: Operation) -> Operation:
        account = self._account_facade.get_account(operation.bank_account_id)
        if operation.type == TransactionType.INCOME:
            account.balance += operation.amount
        else:
            account.balance -= operation.amount
        
        self._account_facade.update_account(account)
        self._repo.add(operation)
        return operation

    def delete_operation(self, operation_id: int):
        self._repo.remove(operation_id)

    def get_operations_by_account(self, account_id: int) -> List[Operation]:
        return [op for op in self._repo.get_all() if op.bank_account_id == account_id]