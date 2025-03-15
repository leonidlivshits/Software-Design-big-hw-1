from dataclasses import dataclass
from Domain.exceptions import DomainException


@dataclass
class BankAccount:
    id: int
    name: str
    balance: float = 0.0

    def __post_init__(self):
        if self.balance < 0:
            raise DomainException("Balance cannot be negative")