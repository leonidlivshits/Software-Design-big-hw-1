from Domain.Entities.BankAccount import BankAccount
from Domain.exceptions import DomainException

class AccountFactory:
    @staticmethod
    def create(id: int, name: str, balance: float = 0.0) -> BankAccount:
        try:
            return BankAccount(id=id, name=name, balance=balance)
        except DomainException as e:
            raise ValueError(str(e)) from e