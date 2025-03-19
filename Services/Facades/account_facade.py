from typing import List, Optional
from Domain.Entities.BankAccount import BankAccount
from Services.Repositories.IRepository import IRepository

class AccountFacade:
    def __init__(self, repository: IRepository[BankAccount]):
        self._repo = repository

    def create_account(self, account_id: int, name: str, balance: float) -> BankAccount:
        account = BankAccount(id=account_id, name=name, balance=balance)
        self._repo.add(account)
        return account

    def get_all_accounts(self) -> List[BankAccount]:
        return self._repo.get_all()

    def get_account(self, account_id: int) -> Optional[BankAccount]:
        return self._repo.get(account_id)

    def delete_account(self, account_id: int):
        self._repo.remove(account_id)

    def delete_account(self, account_id: int):
        self._repo.remove(account_id)

    def update_account(self, account: BankAccount):
        self._repo.remove(account.id)
        self._repo.add(account)